/**
 * AI&DST 2026 Quiz Anti-Cheat Engine
 * Monitored violations: Tab switching, window blur, fullscreen exits, devtools shortcuts.
 * 2-Strike Enforcement: Warning on 1st offense, Instant Disqualification & Lockout on 2nd offense.
 */

class AntiCheatGuard {
  constructor(options = {}) {
    this.isActive = false;
    this.violationCount = 0;
    this.maxStrikes = 2;
    this.lastViolationTime = 0;
    this.onDisqualified = options.onDisqualified || (() => {});
    this.onWarning = options.onWarning || (() => {});
    this.audioCtx = null;
  }

  init() {
    this.setupAudio();
    this.bindEvents();
    this.blockCheatingShortcuts();
  }

  activate() {
    this.isActive = true;
    console.log("🛡️ Anti-Cheat Guard activated. Monitoring tab switching & window focus.");
  }

  deactivate() {
    this.isActive = false;
  }

  setupAudio() {
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        this.audioCtx = new AudioContext();
      }
    } catch (e) {
      console.warn("Web Audio API not supported", e);
    }
  }

  playAlarmSound() {
    try {
      if (!this.audioCtx) this.setupAudio();
      if (this.audioCtx && this.audioCtx.state === 'suspended') {
        this.audioCtx.resume();
      }
      if (this.audioCtx) {
        const osc = this.audioCtx.createOscillator();
        const gain = this.audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(800, this.audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(300, this.audioCtx.currentTime + 0.35);
        gain.gain.setValueAtTime(0.3, this.audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.audioCtx.currentTime + 0.35);
        osc.connect(gain);
        gain.connect(this.audioCtx.destination);
        osc.start();
        osc.stop(this.audioCtx.currentTime + 0.36);
      }
    } catch (e) {
      // Audio playback best effort
    }
  }

  async reportViolation(type, details) {
    if (!this.isActive) return;

    const now = Date.now();
    // Debounce triggers within 3 seconds to avoid double-logging blur + visibilitychange
    if (now - this.lastViolationTime < 3000) {
      return;
    }
    this.lastViolationTime = now;

    this.playAlarmSound();

    try {
      const res = await fetch('/api/report_violation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type, details })
      });

      const data = await res.json();
      if (data.action === 'disqualify') {
        this.isActive = false;
        this.onDisqualified(data.message);
      } else if (data.action === 'warn') {
        this.violationCount = data.violation_count;
        this.onWarning(data.message, this.violationCount, data.max_violations);
      }
    } catch (err) {
      console.error("Failed to report violation", err);
    }
  }

  bindEvents() {
    // 1. Visibility Change (Tab switch or minimization)
    document.addEventListener('visibilitychange', () => {
      if (document.hidden && this.isActive) {
        this.reportViolation('tab_switch', 'Switched browser tab or minimized window');
      }
    });

    // 2. Window Blur (Focus loss to another application)
    window.addEventListener('blur', () => {
      if (this.isActive) {
        this.reportViolation('window_blur', 'Browser lost focus to another window');
      }
    });
  }

  blockCheatingShortcuts() {
    // Disable right click
    document.addEventListener('contextmenu', (e) => {
      if (this.isActive) {
        e.preventDefault();
        return false;
      }
    });

    // Disable copy / paste / select
    document.addEventListener('copy', (e) => {
      if (this.isActive) {
        e.preventDefault();
      }
    });

    // Block keyboard shortcuts (DevTools, Inspect, Print, View Source)
    document.addEventListener('keydown', (e) => {
      if (!this.isActive) return;

      // F12
      if (e.key === 'F12') {
        e.preventDefault();
        this.reportViolation('devtools_attempt', 'Pressed F12 DevTools key');
        return false;
      }

      // Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+Shift+C (Devtools)
      if (e.ctrlKey && e.shiftKey && ['I', 'J', 'C', 'i', 'j', 'c'].includes(e.key)) {
        e.preventDefault();
        this.reportViolation('devtools_attempt', 'Attempted to open Developer Tools');
        return false;
      }

      // Ctrl+U (View Source)
      if (e.ctrlKey && ['u', 'U'].includes(e.key)) {
        e.preventDefault();
        return false;
      }

      // Ctrl+C, Ctrl+V, Ctrl+P
      if (e.ctrlKey && ['c', 'v', 'p', 'C', 'V', 'P'].includes(e.key)) {
        e.preventDefault();
        return false;
      }
    });
  }
}

// Global instance
window.AntiCheatGuard = AntiCheatGuard;
