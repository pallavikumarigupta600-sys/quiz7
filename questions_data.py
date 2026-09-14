"""
Quiz Questions Data (1 to 60)
All 60 questions extracted with full precision from the competition PDF.
Includes options, answers, passages, code snippets, and SVG images for logo questions.
"""

QUESTIONS = [
    {
        "id": 1,
        "category": "English & Verbal",
        "question": "Choose the word closest in meaning to \"BRIEF\".",
        "options": {
            "A": "Long",
            "B": "Short",
            "C": "Difficult",
            "D": "Strong"
        },
        "answer": "B"
    },
    {
        "id": 2,
        "category": "English & Verbal",
        "question": "Choose the opposite of \"ANCIENT\".",
        "options": {
            "A": "Old",
            "B": "Historic",
            "C": "Modern",
            "D": "Traditional"
        },
        "answer": "C"
    },
    {
        "id": 3,
        "category": "English & Verbal",
        "question": "Choose the correctly arranged sentence:\nP. to the library  Q. every evening  R. goes Rahul  S. to study",
        "options": {
            "A": "R-P-S-Q",
            "B": "P-R-Q-S",
            "C": "R-S-P-Q",
            "D": "Q-R-P-S"
        },
        "answer": "A"
    },
    {
        "id": 4,
        "category": "English & Verbal",
        "question": "She is good ___ mathematics.",
        "options": {
            "A": "in",
            "B": "at",
            "C": "on",
            "D": "for"
        },
        "answer": "B"
    },
    {
        "id": 5,
        "category": "English & Verbal",
        "question": "If I ___ enough time, I would help you.",
        "options": {
            "A": "have",
            "B": "had",
            "C": "will have",
            "D": "having"
        },
        "answer": "B"
    },
    {
        "id": 6,
        "category": "English & Verbal",
        "question": "The manager has been working here ___ 2020.",
        "options": {
            "A": "for",
            "B": "from",
            "C": "since",
            "D": "by"
        },
        "answer": "C"
    },
    {
        "id": 7,
        "category": "English & Verbal",
        "question": "By the time we reached the station, the train ___.",
        "options": {
            "A": "leaves",
            "B": "has left",
            "C": "had left",
            "D": "will leave"
        },
        "answer": "C"
    },
    {
        "id": 8,
        "category": "English & Verbal",
        "question": "She ___ for the exam since morning.",
        "options": {
            "A": "studies",
            "B": "studied",
            "C": "has been studying",
            "D": "will study"
        },
        "answer": "C"
    },
    {
        "id": 9,
        "category": "English & Verbal",
        "question": "I ___ this movie twice already.",
        "options": {
            "A": "watched",
            "B": "have watched",
            "C": "watch",
            "D": "had watching"
        },
        "answer": "B"
    },
    {
        "id": 10,
        "category": "English & Verbal",
        "question": "Change into Passive Voice: “The chef prepared the meal.”",
        "options": {
            "A": "The meal is prepared by the chef.",
            "B": "The meal was prepared by the chef.",
            "C": "The meal has prepared by the chef.",
            "D": "The chef was prepared by the meal."
        },
        "answer": "B"
    },
    {
        "id": 11,
        "category": "English & Verbal",
        "question": "Change into Active Voice: “The project was completed by the students.”",
        "options": {
            "A": "The students complete the project.",
            "B": "The students completed the project.",
            "C": "The students have completed the project.",
            "D": "The students were completing the project."
        },
        "answer": "B"
    },
    {
        "id": 12,
        "category": "English & Verbal",
        "question": "Change into Passive Voice: “They are building a new bridge.”",
        "options": {
            "A": "A new bridge is being built by them.",
            "B": "A new bridge was built by them.",
            "C": "A new bridge has been built by them.",
            "D": "A new bridge is built by them."
        },
        "answer": "A"
    },
    {
        "id": 13,
        "category": "Reading Comprehension",
        "passage": "Success is often associated with talent, but talent alone rarely determines the outcome. People who consistently practice, learn from their mistakes, and adapt to changing circumstances often achieve more than those who depend only on natural ability. Failure, therefore, should not always be viewed as the opposite of success. It can provide valuable information about what needs to be improved.",
        "question": "Passage Comprehension:\nThe word “adapt” in the passage most nearly means:",
        "options": {
            "A": "Refuse to change",
            "B": "Adjust to new situations",
            "C": "Forget previous experiences",
            "D": "Stop learning"
        },
        "answer": "B"
    },
    {
        "id": 14,
        "category": "Reading Comprehension",
        "passage": "Success is often associated with talent, but talent alone rarely determines the outcome. People who consistently practice, learn from their mistakes, and adapt to changing circumstances often achieve more than those who depend only on natural ability. Failure, therefore, should not always be viewed as the opposite of success. It can provide valuable information about what needs to be improved.",
        "question": "Which statement is supported by the passage?",
        "options": {
            "A": "Natural ability guarantees success",
            "B": "Practice can help people overcome limitations",
            "C": "Mistakes should always be avoided",
            "D": "Failure has no value"
        },
        "answer": "B"
    },
    {
        "id": 15,
        "category": "Reading Comprehension",
        "passage": "Success is often associated with talent, but talent alone rarely determines the outcome. People who consistently practice, learn from their mistakes, and adapt to changing circumstances often achieve more than those who depend only on natural ability. Failure, therefore, should not always be viewed as the opposite of success. It can provide valuable information about what needs to be improved.",
        "question": "What can be inferred about a person who learns from mistakes?",
        "options": {
            "A": "They are more likely to improve over time",
            "B": "They never make mistakes again",
            "C": "They depend only on talent",
            "D": "They avoid challenges"
        },
        "answer": "A"
    },
    {
        "id": 16,
        "category": "Entertainment & Pop Culture",
        "question": "In Jersey, what is the name of the son of Arjun?",
        "options": {
            "A": "Nani",
            "B": "Kittu",
            "C": "Karthik",
            "D": "Raman"
        },
        "answer": "B"
    },
    {
        "id": 17,
        "category": "Entertainment & Pop Culture",
        "question": "Who composed the music for Arjun Reddy?",
        "options": {
            "A": "Radhan",
            "B": "Vivek Sagar",
            "C": "Gopi Sundar",
            "D": "Anirudh"
        },
        "answer": "A"
    },
    {
        "id": 18,
        "category": "Aptitude & Logic",
        "question": "What is the angle between the hour hand and minute hand at 3:30?",
        "options": {
            "A": "75°",
            "B": "90°",
            "C": "105°",
            "D": "120°"
        },
        "answer": "A"
    },
    {
        "id": 19,
        "category": "Aptitude & Logic",
        "question": "A father is 3 times as old as his son. After 10 years, the father will be twice as old as his son. What is the son's present age?",
        "options": {
            "A": "8 years",
            "B": "10 years",
            "C": "12 years",
            "D": "15 years"
        },
        "answer": "B"
    },
    {
        "id": 20,
        "category": "Aptitude & Logic",
        "question": "Three boxes are labelled: APPLES, ORANGES, APPLES+ORANGES. All three labels are wrong. You can pick only one fruit from one box without looking inside. Which box should you pick from to correctly identify all three boxes?",
        "options": {
            "A": "APPLES",
            "B": "ORANGES",
            "C": "APPLES + ORANGES",
            "D": "Any box"
        },
        "answer": "C"
    },
    {
        "id": 21,
        "category": "Aptitude & Logic",
        "question": "A room has 5 candles. You blow out 2 candles. How many candles remain?",
        "options": {
            "A": "2",
            "B": "3",
            "C": "5",
            "D": "0"
        },
        "answer": "C"
    },
    {
        "id": 22,
        "category": "Entertainment & Pop Culture",
        "question": "Guess the Movie: A hero works with red sandalwood, a police officer keeps chasing him, and the hero says “Thaggede Le.”",
        "options": {
            "A": "Pushpa",
            "B": "Rangasthalam",
            "C": "Dasara",
            "D": "Devara"
        },
        "answer": "A"
    },
    {
        "id": 23,
        "category": "Entertainment & Pop Culture",
        "question": "Which Disney character is known for saying “Hakuna Matata”?",
        "options": {
            "A": "Simba",
            "B": "Olaf",
            "C": "Aladdin",
            "D": "Stitch"
        },
        "answer": "A"
    },
    {
        "id": 24,
        "category": "Entertainment & Pop Culture",
        "question": "Guess the Telugu Movie from Emojis:\n👰 🤵 👀 🍵 🎬",
        "options": {
            "A": "Pelli Choopulu",
            "B": "Geetha Govindam",
            "C": "Fidaa",
            "D": "Pellichoopulu 2"
        },
        "answer": "A"
    },
    {
        "id": 25,
        "category": "Aptitude & Logic",
        "question": "A person is looking at a photograph. Someone asks, “Who is in the picture?” He replies: “I have no brothers or sisters, but that person's father is my father's son.” Who is in the photograph?",
        "options": {
            "A": "His father",
            "B": "His son",
            "C": "Himself",
            "D": "His uncle"
        },
        "answer": "B"
    },
    {
        "id": 26,
        "category": "Aptitude & Logic",
        "question": "Which month has 28 days?",
        "options": {
            "A": "February",
            "B": "January",
            "C": "June",
            "D": "None of the above"
        },
        "answer": "D"
    },
    {
        "id": 27,
        "category": "General Knowledge",
        "question": "Which country was the first to adopt a written constitution?",
        "options": {
            "A": "USA",
            "B": "France",
            "C": "San Marino",
            "D": "Switzerland"
        },
        "answer": "C"
    },
    {
        "id": 28,
        "category": "General Knowledge & History",
        "question": "The “Doctrine of Lapse” was introduced by which British Governor-General?",
        "options": {
            "A": "Lord Curzon",
            "B": "Lord Dalhousie",
            "C": "Lord Wellesley",
            "D": "Lord Canning"
        },
        "answer": "B"
    },
    {
        "id": 29,
        "category": "General Science & Astronomy",
        "question": "Which is the only planet in our Solar System that rotates clockwise?",
        "options": {
            "A": "Mars",
            "B": "Venus",
            "C": "Jupiter",
            "D": "Neptune"
        },
        "answer": "B"
    },
    {
        "id": 30,
        "category": "General Knowledge",
        "question": "Who was the first Indian to win a Nobel Prize?",
        "options": {
            "A": "C. V. Raman",
            "B": "Rabindranath Tagore",
            "C": "Mother Teresa",
            "D": "Amartya Sen"
        },
        "answer": "B"
    },
    {
        "id": 31,
        "category": "Indian Polity & Constitution",
        "question": "Which Article of the Indian Constitution deals with the abolition of untouchability?",
        "options": {
            "A": "Article 14",
            "B": "Article 15",
            "C": "Article 17",
            "D": "Article 21"
        },
        "answer": "C"
    },
    {
        "id": 32,
        "category": "Geography",
        "question": "Which Indian state has the longest coastline?",
        "options": {
            "A": "Andhra Pradesh",
            "B": "Tamil Nadu",
            "C": "Gujarat",
            "D": "Maharashtra"
        },
        "answer": "C"
    },
    {
        "id": 33,
        "category": "International Organizations",
        "question": "The headquarters of the International Court of Justice is located in:",
        "options": {
            "A": "Geneva",
            "B": "New York",
            "C": "Paris",
            "D": "The Hague"
        },
        "answer": "D"
    },
    {
        "id": 34,
        "category": "Science & Chemistry",
        "question": "Which element has the highest melting point?",
        "options": {
            "A": "Iron",
            "B": "Tungsten",
            "C": "Platinum",
            "D": "Titanium"
        },
        "answer": "B"
    },
    {
        "id": 35,
        "category": "Science & Physics",
        "question": "Who discovered the neutron?",
        "options": {
            "A": "Ernest Rutherford",
            "B": "J. J. Thomson",
            "C": "James Chadwick",
            "D": "Niels Bohr"
        },
        "answer": "C"
    },
    {
        "id": 36,
        "category": "Geography",
        "question": "Which is the deepest ocean trench in the world?",
        "options": {
            "A": "Tonga Trench",
            "B": "Mariana Trench",
            "C": "Philippine Trench",
            "D": "Java Trench"
        },
        "answer": "B"
    },
    {
        "id": 37,
        "category": "General Knowledge",
        "question": "The term “Blue Revolution” is associated with:",
        "options": {
            "A": "Milk production",
            "B": "Fish production",
            "C": "Oil production",
            "D": "Wheat production"
        },
        "answer": "B"
    },
    {
        "id": 38,
        "category": "Art & Culture",
        "question": "Which Indian classical dance originated in Kerala?",
        "options": {
            "A": "Kathak",
            "B": "Bharatanatyam",
            "C": "Kathakali",
            "D": "Odissi"
        },
        "answer": "C"
    },
    {
        "id": 39,
        "category": "International Affairs",
        "question": "Who was the first woman President of the United Nations General Assembly?",
        "options": {
            "A": "Indira Gandhi",
            "B": "Vijaya Lakshmi Pandit",
            "C": "Golda Meir",
            "D": "Eleanor Roosevelt"
        },
        "answer": "B"
    },
    {
        "id": 40,
        "category": "Science & Chemistry",
        "question": "Which metal is known as “Quicksilver”?",
        "options": {
            "A": "Silver",
            "B": "Mercury",
            "C": "Lead",
            "D": "Zinc"
        },
        "answer": "B"
    },
    {
        "id": 41,
        "category": "Astronomy & Space",
        "question": "The “Great Red Spot” is a feature of which planet?",
        "options": {
            "A": "Saturn",
            "B": "Jupiter",
            "C": "Uranus",
            "D": "Neptune"
        },
        "answer": "B"
    },
    {
        "id": 42,
        "category": "Computer Science - C Programming",
        "question": "What will be the output?",
        "code_snippet": "int x = 5;\nprintf(\"%d %d\", x++, ++x);",
        "options": {
            "A": "5 7",
            "B": "6 7",
            "C": "5 6",
            "D": "Undefined behavior"
        },
        "answer": "D"
    },
    {
        "id": 43,
        "category": "Computer Science - C Programming",
        "question": "C Programming: Which storage class allows a variable to retain its value between function calls?",
        "options": {
            "A": "auto",
            "B": "register",
            "C": "static",
            "D": "extern"
        },
        "answer": "C"
    },
    {
        "id": 44,
        "category": "Computer Science - C Programming",
        "question": "C Programming: What is the size of a pointer on a typical 64-bit system?",
        "options": {
            "A": "2 bytes",
            "B": "4 bytes",
            "C": "8 bytes",
            "D": "Depends on the data type"
        },
        "answer": "C"
    },
    {
        "id": 45,
        "category": "Computer Science - Data Structures",
        "question": "Data Structures: What is the worst-case time complexity of searching in a balanced Binary Search Tree?",
        "options": {
            "A": "O(1)",
            "B": "O(log n)",
            "C": "O(n)",
            "D": "O(n log n)"
        },
        "answer": "B"
    },
    {
        "id": 46,
        "category": "Computer Science - Data Structures",
        "question": "Data Structures: Which data structure is used internally by BFS?",
        "options": {
            "A": "Stack",
            "B": "Queue",
            "C": "Heap",
            "D": "Hash Table"
        },
        "answer": "B"
    },
    {
        "id": 47,
        "category": "Computer Science - Algorithms",
        "question": "Algorithms: What is the worst-case time complexity of Quick Sort?",
        "options": {
            "A": "O(n log n)",
            "B": "O(n²)",
            "C": "O(log n)",
            "D": "O(n)"
        },
        "answer": "B"
    },
    {
        "id": 48,
        "category": "Computer Science - Algorithms",
        "question": "Algorithms: Which algorithm is commonly used to find the shortest path in a graph with non-negative edge weights?",
        "options": {
            "A": "Prim's",
            "B": "Kruskal's",
            "C": "Dijkstra's",
            "D": "Floyd's"
        },
        "answer": "C"
    },
    {
        "id": 49,
        "category": "Computer Science - DBMS",
        "question": "DBMS: Which normal form eliminates partial dependency?",
        "options": {
            "A": "1NF",
            "B": "2NF",
            "C": "3NF",
            "D": "BCNF"
        },
        "answer": "B"
    },
    {
        "id": 50,
        "category": "Computer Science - DBMS",
        "question": "DBMS: Which SQL command removes a table and its structure?",
        "options": {
            "A": "DELETE",
            "B": "REMOVE",
            "C": "DROP",
            "D": "TRUNCATE"
        },
        "answer": "C"
    },
    {
        "id": 51,
        "category": "Computer Science - DBMS",
        "question": "DBMS: Which property of a database transaction ensures that a committed transaction survives system failure?",
        "options": {
            "A": "Atomicity",
            "B": "Consistency",
            "C": "Isolation",
            "D": "Durability"
        },
        "answer": "D"
    },
    {
        "id": 52,
        "category": "Computer Science - Operating Systems",
        "question": "Operating Systems: Which algorithm can suffer from Belady's Anomaly?",
        "options": {
            "A": "LRU",
            "B": "FIFO",
            "C": "Optimal",
            "D": "MRU"
        },
        "answer": "B"
    },
    {
        "id": 53,
        "category": "Computer Science - Operating Systems",
        "question": "Operating Systems: A process waiting indefinitely for a resource held by another process is involved in:",
        "options": {
            "A": "Starvation",
            "B": "Deadlock",
            "C": "Thrashing",
            "D": "Paging"
        },
        "answer": "B"
    },
    {
        "id": 54,
        "category": "Computer Science - Operating Systems",
        "question": "Operating Systems: Which scheduling algorithm gives each process a fixed time slice?",
        "options": {
            "A": "FCFS",
            "B": "SJF",
            "C": "Round Robin",
            "D": "Priority Scheduling"
        },
        "answer": "C"
    },
    {
        "id": 55,
        "category": "Computer Science - Computer Networks",
        "question": "Computer Networks: Which protocol translates a domain name such as google.com into an IP address?",
        "options": {
            "A": "DHCP",
            "B": "DNS",
            "C": "ARP",
            "D": "FTP"
        },
        "answer": "B"
    },
    {
        "id": 56,
        "category": "Computer Science - Computer Networks",
        "question": "Computer Networks: Which layer of the OSI model is responsible for routing?",
        "options": {
            "A": "Data Link",
            "B": "Network",
            "C": "Transport",
            "D": "Session"
        },
        "answer": "B"
    },
    {
        "id": 57,
        "category": "Visual Logo Identification",
        "question": "Identify the logo:",
        "image_svg": '''<svg viewBox="0 0 200 200" width="160" height="160" xmlns="http://www.w3.org/2000/svg">
  <circle cx="100" cy="100" r="90" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>
  <circle cx="100" cy="100" r="75" fill="none" stroke="#94a3b8" stroke-dasharray="8 6" stroke-width="3"/>
  <path d="M 60 70 Q 100 45 140 70 Q 155 110 135 145 Q 100 165 65 145 Q 45 110 60 70 Z" fill="#e2e8f0" stroke="#64748b" stroke-width="2"/>
  <text x="78" y="95" font-size="28" font-family="serif" font-weight="bold" fill="#334155">W</text>
  <text x="110" y="98" font-size="24" font-family="serif" fill="#475569">Ω</text>
  <text x="76" y="132" font-size="22" font-family="sans-serif" fill="#475569">維</text>
  <text x="112" y="132" font-size="22" font-family="serif" fill="#334155">И</text>
  <path d="M 98 50 L 98 150 M 55 100 L 145 100" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3 3"/>
</svg>''',
        "options": {
            "A": "Wikipedia",
            "B": "Google",
            "C": "Facebook",
            "D": "Twitter"
        },
        "answer": "A"
    },
    {
        "id": 58,
        "category": "Visual Logo Identification",
        "question": "Identify the logo:",
        "image_svg": '''<svg viewBox="0 0 200 200" width="160" height="160" xmlns="http://www.w3.org/2000/svg">
  <rect width="200" height="200" rx="20" fill="#ffffff"/>
  <!-- Panda Head & Body stylized silhouette -->
  <ellipse cx="100" cy="120" rx="42" ry="36" fill="#111827"/>
  <ellipse cx="100" cy="105" rx="30" ry="24" fill="#ffffff"/>
  <!-- Ears -->
  <circle cx="76" cy="65" r="14" fill="#111827"/>
  <circle cx="124" cy="65" r="14" fill="#111827"/>
  <!-- Head -->
  <circle cx="100" cy="84" r="28" fill="#ffffff" stroke="#111827" stroke-width="4"/>
  <!-- Eye patches -->
  <ellipse cx="89" cy="82" rx="7" ry="10" transform="rotate(-18 89 82)" fill="#111827"/>
  <ellipse cx="111" cy="82" rx="7" ry="10" transform="rotate(18 111 82)" fill="#111827"/>
  <!-- Nose -->
  <ellipse cx="100" cy="94" rx="4" ry="3" fill="#111827"/>
  <!-- Limbs -->
  <ellipse cx="68" cy="124" rx="16" ry="24" fill="#111827"/>
  <ellipse cx="132" cy="124" rx="16" ry="24" fill="#111827"/>
  <ellipse cx="84" cy="148" rx="14" ry="12" fill="#111827"/>
  <ellipse cx="116" cy="148" rx="14" ry="12" fill="#111827"/>
  <text x="100" y="182" font-size="18" font-family="Arial, sans-serif" font-weight="900" letter-spacing="4" text-anchor="middle" fill="#111827">WWF</text>
</svg>''',
        "options": {
            "A": "WWF",
            "B": "Greenpeace",
            "C": "National Geographic",
            "D": "UNICEF"
        },
        "answer": "A"
    },
    {
        "id": 59,
        "category": "Visual Logo Identification",
        "question": "Identify the logo:",
        "image_svg": '''<svg viewBox="0 0 200 200" width="160" height="160" xmlns="http://www.w3.org/2000/svg">
  <circle cx="100" cy="100" r="85" fill="#fbb034" stroke="#05164d" stroke-width="6"/>
  <!-- Stylized crane in flight -->
  <path d="M 45 108 C 65 95, 90 92, 115 95 C 135 70, 155 52, 158 50 C 158 50, 150 78, 140 92 C 152 93, 162 90, 165 88 C 160 98, 146 104, 130 106 C 115 108, 92 112, 75 125 C 65 133, 55 145, 52 152 C 54 138, 55 124, 45 108 Z" fill="#05164d"/>
  <circle cx="100" cy="100" r="72" fill="none" stroke="#05164d" stroke-width="4"/>
</svg>''',
        "options": {
            "A": "Lufthansa",
            "B": "Emirates",
            "C": "Qatar Airways",
            "D": "Air India"
        },
        "answer": "A"
    },
    {
        "id": 60,
        "category": "Visual Logo Identification",
        "question": "Identify the logo:",
        "image_svg": '''<svg viewBox="0 0 200 200" width="160" height="160" xmlns="http://www.w3.org/2000/svg">
  <rect width="200" height="200" rx="20" fill="#ffffff"/>
  <!-- Interlocking Double C Logo -->
  <g stroke="#000000" stroke-width="16" fill="none" stroke-linecap="round">
    <!-- First C opening to the right -->
    <path d="M 115 65 A 40 40 0 1 0 115 135"/>
    <!-- Second C opening to the left (mirrored) -->
    <path d="M 85 65 A 40 40 0 1 1 85 135"/>
  </g>
</svg>''',
        "options": {
            "A": "Chanel",
            "B": "Gucci",
            "C": "Louis Vuitton",
            "D": "Dior"
        },
        "answer": "A"
    }
]

TEAM_CREDENTIALS = {
    f"team{i}": "AI&DST2026" for i in range(1, 21)
}

ADMIN_CREDENTIALS = {
    "MAHA": "AI&DSA2026",
    "admin": "AI&DSA2026"
}
