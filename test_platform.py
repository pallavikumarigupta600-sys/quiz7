"""
Comprehensive Test Suite for AI&DST 2026 Quiz Platform
Tests all authentication, timer, anti-cheat, master switch, answer saving, score calculation, and admin inspection endpoints.
"""

import sys
import json
import unittest
from app import app, init_db, get_db

class QuizPlatformTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        init_db()
        conn = get_db()
        conn.execute("DELETE FROM answers")
        conn.execute("DELETE FROM violations")
        conn.execute("UPDATE teams SET status = 'waiting', start_time = NULL, end_time = NULL, score = 0, violations_count = 0, disqualified_reason = NULL")
        conn.execute("UPDATE config SET value = '0' WHERE key = 'competition_active'")
        conn.commit()
        conn.close()

    def test_01_logins(self):
        # Admin login
        res = self.client.post('/login', json={'username': 'MAHA', 'password': 'AI&DSA2026'})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['role'], 'admin')

        # Invalid login
        res_fail = self.client.post('/login', json={'username': 'team1', 'password': 'wrongpassword'})
        self.assertEqual(res_fail.status_code, 401)

        # Team login
        res_team = self.client.post('/login', json={'username': 'team1', 'password': 'AI&DST2026'})
        self.assertEqual(res_team.status_code, 200)
        data_team = res_team.get_json()
        self.assertTrue(data_team['success'])
        self.assertEqual(data_team['role'], 'team')

    def test_02_master_switch_and_exam_flow(self):
        # 1. Team logs in before admin starts competition
        with self.client.session_transaction() as sess:
            sess['user'] = 'team2'
            sess['role'] = 'team'

        # Competition is initially idle
        conn = get_db()
        conn.execute("UPDATE config SET value = '0' WHERE key = 'competition_active'")
        conn.commit()
        conn.close()

        res_start = self.client.post('/api/start_quiz')
        self.assertEqual(res_start.status_code, 403)
        self.assertIn("not started", res_start.get_json()['error'])

        # 2. Admin starts competition
        with self.client.session_transaction() as sess:
            sess['user'] = 'MAHA'
            sess['role'] = 'admin'
        res_admin_start = self.client.post('/api/admin/start_competition')
        self.assertEqual(res_admin_start.status_code, 200)

        # 3. Team2 starts exam now
        with self.client.session_transaction() as sess:
            sess['user'] = 'team2'
            sess['role'] = 'team'
        res_team_start = self.client.post('/api/start_quiz')
        self.assertEqual(res_team_start.status_code, 200)
        start_data = res_team_start.get_json()
        self.assertTrue(start_data['success'])
        self.assertGreaterEqual(start_data['remaining_seconds'], 3590)

        # 4. Check questions (60 questions, no answers revealed)
        res_q = self.client.get('/api/questions')
        self.assertEqual(res_q.status_code, 200)
        q_data = res_q.get_json()
        self.assertEqual(len(q_data['questions']), 60)
        self.assertNotIn('answer', q_data['questions'][0])

        # 5. Save answers: Q1 (correct 'B'), Q2 (correct 'C')
        res_ans1 = self.client.post('/api/save_answer', json={
            'question_id': 1,
            'selected_option': 'B',
            'marked_for_review': False
        })
        self.assertEqual(res_ans1.status_code, 200)

        res_ans2 = self.client.post('/api/save_answer', json={
            'question_id': 2,
            'selected_option': 'C',
            'marked_for_review': True
        })
        self.assertEqual(res_ans2.status_code, 200)

        # Verify score is now 2
        conn = get_db()
        team_row = conn.execute("SELECT score FROM teams WHERE username = 'team2'").fetchone()
        self.assertEqual(team_row['score'], 2)
        conn.close()

        # 6. Anti-Cheat test: 1st violation (Warning)
        res_v1 = self.client.post('/api/report_violation', json={'type': 'tab_switch', 'details': 'Switched tab'})
        self.assertEqual(res_v1.status_code, 200)
        self.assertEqual(res_v1.get_json()['action'], 'warn')

        # 2nd violation (Disqualification)
        # Advance time slightly to bypass debounce
        import time
        time.sleep(0.05)
        res_v2 = self.client.post('/api/report_violation', json={'type': 'window_blur', 'details': 'Minimized window'})
        self.assertEqual(res_v2.status_code, 200)
        self.assertEqual(res_v2.get_json()['action'], 'disqualify')

        # Check team status in DB
        conn = get_db()
        disq_row = conn.execute("SELECT status, violations_count FROM teams WHERE username = 'team2'").fetchone()
        self.assertEqual(disq_row['status'], 'disqualified')
        self.assertEqual(disq_row['violations_count'], 2)
        conn.close()

        # 7. Admin inspection
        with self.client.session_transaction() as sess:
            sess['user'] = 'MAHA'
            sess['role'] = 'admin'
        res_details = self.client.get('/api/admin/team_details/team2')
        self.assertEqual(res_details.status_code, 200)
        det_data = res_details.get_json()
        self.assertEqual(det_data['team']['status'], 'disqualified')
        self.assertEqual(det_data['breakdown'][0]['status'], 'correct')
        self.assertEqual(det_data['breakdown'][1]['status'], 'correct')
        self.assertEqual(len(det_data['violations']), 2)

        # 8. Admin unlocks team2
        res_unlock = self.client.post('/api/admin/reset_team', json={'team_id': 'team2', 'action_type': 'unlock'})
        self.assertEqual(res_unlock.status_code, 200)

        # 9. Team2 submits quiz
        with self.client.session_transaction() as sess:
            sess['user'] = 'team2'
            sess['role'] = 'team'
        res_submit = self.client.post('/api/submit_quiz', json={'auto_submit': False})
        self.assertEqual(res_submit.status_code, 200)
        sub_data = res_submit.get_json()
        self.assertTrue(sub_data['success'])
        self.assertEqual(sub_data['score'], 2)

        # 10. Admin exports CSV
        with self.client.session_transaction() as sess:
            sess['user'] = 'MAHA'
            sess['role'] = 'admin'
        res_csv = self.client.get('/api/admin/export_csv')
        self.assertEqual(res_csv.status_code, 200)
        self.assertIn("team2", res_csv.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
