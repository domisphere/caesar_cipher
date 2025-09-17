# 🔐 ROT Cipher Manager

A simple Python project for encrypting and decrypting text using **ROT13** and **ROT47** ciphers.
The program allows you to add texts, manage a buffer, save to JSON files, and load them back.

---


## 🚀 Installation & Run

1. Clone the repository:
   ```bash
   git clone https://github.com/domisphere/caesar_cipher.git
   cd caesar_cipher
   ```
2. Run:
   ```bash
   pip install -r requirements.txt
   python main.py
   ```


## 📌 Example Usage

```
--- MENU ---
1. Add text
2. Show buffer
3. Encrypt/Decrypt
4. Save to file
5. Load from file
6. Exit

Choose an option: 1
Enter text: Hello World
Text 'Hello World' has been added to the buffer
```


## 📂 Project Structure

```
caesar_cipher/
├── src/
│   ├── cipher.py
│   ├── manager.py
│   ├── buffer.py
│   ├── text.py
│   ├── menu.py
│   ├── constants.py
│   ├── exceptions.py
│   └── file_handler.py
├── tests/
│   ├── test_cipher.py
│   ├── test_manager.py
│   ├── test_buffer.py
│   ├── test_text.py
│   ├── test_menu.py
│   └── test_file_handler.py
├── data/
│   └── .gitkeep
├── main.py
├── README.md
├── requirements.txt
├── .pre-commit-config.yaml
├── pyproject.toml
└── .github/
    └── workflows/
        └── ci.yml

```


## 👤 Author
Dominik Rząsa
