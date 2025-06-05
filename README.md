# PDF Password Cracker 🔓

A powerful and efficient Python tool to crack password-protected PDF files using wordlist attacks and brute force methods with multithreading support.

## ⚠️ Legal Disclaimer

**This tool is for educational and authorized testing purposes only.**

- Only use on PDF files you own or have explicit permission to test
- Unauthorized access to protected documents is illegal
- Users are responsible for compliance with local laws and regulations
- The developers assume no liability for misuse of this tool

## 🚀 Features

- 📝 **Wordlist Attack**: Use custom wordlists for targeted password cracking
- 🔢 **Brute Force Attack**: Generate passwords with customizable character sets and lengths
- ⚡ **Multithreading**: Parallel processing for faster cracking (configurable thread count)
- 📊 **Progress Tracking**: Real-time progress bar with speed metrics
- ⏹️ **Graceful Interruption**: Clean shutdown with Ctrl+C support
- 🛡️ **Input Validation**: Comprehensive error handling and file validation
- 🎯 **Smart Defaults**: Optimized default settings for common scenarios
- 📈 **Performance Metrics**: Shows passwords tried per second and estimated time

## 🛠️ Installation

### Prerequisites

- Python 3.6 or higher
- pip package manager

### Required Dependencies

```bash
pip install pikepdf tqdm
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

**requirements.txt:**

```
pikepdf>=8.0.0
tqdm>=4.64.0
```

### Clone the Repository

```bash
git clone https://github.com/AkshayRane05/PDF_Password_Cracker.git
cd PDF_Password_Cracker
```

## 📖 Usage

### Basic Syntax

```bash
python pdf_cracker.py <pdf_file> [options]
```

### Wordlist Attack

```bash
python pdf_cracker.py protected.pdf -w passwords.txt
```

### Brute Force Attack

```bash
python pdf_cracker.py protected.pdf -g -min 1 -max 4 -c "0123456789"
```

## 🎯 Examples

### 1. **Dictionary Attack with Common Passwords**

```bash
python pdf_cracker.py document.pdf -w rockyou.txt -t 8
```

### 2. **Brute Force Numeric PIN (4-6 digits)**

```bash
python pdf_cracker.py secure.pdf -g -min 4 -max 6 -c "0123456789"
```

### 3. **Brute Force Alphanumeric (lowercase + numbers)**

```bash
python pdf_cracker.py protected.pdf -g -min 1 -max 4 -c "abcdefghijklmnopqrstuvwxyz0123456789"
```

### 4. **Custom Character Set (letters + special chars)**

```bash
python pdf_cracker.py file.pdf -g -min 3 -max 5 -c "ABCabc123!@#"
```

### 5. **High-Performance Wordlist Attack**

```bash
python pdf_cracker.py target.pdf -w huge_wordlist.txt -t 16
```

## 🔧 Command Line Options

| Option          | Short  | Description                   | Default     |
| --------------- | ------ | ----------------------------- | ----------- |
| `--wordlist`    | `-w`   | Path to wordlist file         | None        |
| `--generate`    | `-g`   | Enable brute force generation | False       |
| `--min-length`  | `-min` | Minimum password length       | 1           |
| `--max-length`  | `-max` | Maximum password length       | 4           |
| `--charset`     | `-c`   | Characters for generation     | `a-z + 0-9` |
| `--max-workers` | `-t`   | Number of threads             | 4           |

## 📊 Performance Guide

### **Thread Optimization**

- **2-4 threads**: Good for basic cracking
- **4-8 threads**: Optimal for most systems
- **8-16 threads**: High-performance systems only
- **16+ threads**: May cause diminishing returns

### **Character Set Recommendations**

- **Numeric only** (`0-9`): Fastest, good for PINs
- **Lowercase + numbers** (`a-z0-9`): Balanced speed/coverage
- **Mixed case + numbers** (`A-Za-z0-9`): Slower but comprehensive
- **Full ASCII**: Very slow, use only for short passwords

### **Expected Performance**

- **Wordlist**: 100-1000+ passwords/second
- **Brute Force**: Depends on character set size
  - 4-digit numeric: ~10,000 combinations
  - 4-char lowercase+numbers: ~1.68M combinations
  - 6-char full ASCII: ~735B combinations

## 🎮 Sample Output

```
[*] Loading wordlist: passwords.txt
[*] Total passwords in wordlist: 14,344,391
[*] Using 8 worker threads
[*] Starting password cracking... (Press Ctrl+C to stop)
Cracking PDF: 45%|████████████▌              | 6,455,176/14,344,391 pwd [02:15<02:45, 47.8Kpwd/s]

[+] Password found: admin123

[+] SUCCESS! Password found: 'admin123'
```

## 📁 Project Structure

```
PDF_Password_Cracker/
├── pdf_cracker.py           # Main cracking script
├── requirements.txt         # Python dependencies
├── passwords.txt           # Sample wordlist for testing
├── README.md              # This documentation
└── examples/              # Example files and scripts
    ├── test_protected.pdf # Sample encrypted PDF
    └── create_test_pdf.py # Script to create test files
```

## 🧪 Testing

### Create Test PDF

First, create a password-protected PDF for testing:

```bash
# Using the PDF Protection Tool
python -c "
import pikepdf
pdf = pikepdf.new()
pdf.pages.append(pikepdf.Page.empty_page(pdf, 200, 300))
pdf.save('test.pdf', encryption={'user': 'password123'})
"
```

### Test the Cracker

```bash
python pdf_cracker.py test.pdf -w passwords.txt
```

## ⚡ Tips for Effective Cracking

1. **Start with wordlists** - Much faster than brute force
2. **Use common password lists** - rockyou.txt, SecLists, etc.
3. **Target specific patterns** - If you know password format
4. **Monitor system resources** - Don't over-thread
5. **Use realistic character sets** - Most passwords use limited chars
6. **Try variations** - Add numbers/symbols to dictionary words

## 🛡️ Security Notes

- **This tool demonstrates PDF security weaknesses**
- **Strong passwords significantly increase cracking time**
- **Consider using certificate-based PDF encryption for sensitive documents**
- **Modern PDFs with AES-256 encryption are much harder to crack**

## 🔍 Troubleshooting

### Common Issues

| Problem                        | Solution                                        |
| ------------------------------ | ----------------------------------------------- |
| `ModuleNotFoundError: pikepdf` | Run `pip install pikepdf`                       |
| PDF not password protected     | Tool will detect and notify                     |
| Wordlist file not found        | Check file path and permissions                 |
| Out of memory errors           | Reduce thread count with `-t`                   |
| Very slow performance          | Try smaller character set or shorter max length |

### Performance Issues

- **Reduce thread count** if system becomes unresponsive
- **Use SSD storage** for large wordlists
- **Close other applications** to free up resources
- **Monitor CPU and RAM usage**

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- **GPU acceleration** using CUDA/OpenCL
- **Smart password generation** using common patterns
- **Resume functionality** for interrupted sessions
- **Multiple PDF batch processing**
- **Additional encryption algorithm support**

### Development Setup

```bash
git clone https://github.com/AkshayRane05/PDF_Password_Cracker.git
cd PDF_Password_Cracker
pip install -r requirements.txt
python pdf_cracker.py --help
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ Ethical Usage

This tool is provided for:

- ✅ Educational purposes and learning about PDF security
- ✅ Testing your own PDF files
- ✅ Authorized penetration testing with proper permissions
- ✅ Security research and vulnerability assessment

**NOT for:**

- ❌ Unauthorized access to others' documents
- ❌ Breaking into systems you don't own
- ❌ Any illegal activities

## 🙏 Acknowledgments

- [pikepdf](https://github.com/pikepdf/pikepdf) - Excellent Python PDF library
- [tqdm](https://github.com/tqdm/tqdm) - Beautiful progress bars
- Security research community for password analysis insights

## 📞 Contact

- **GitHub**: [@AkshayRane05](https://github.com/AkshayRane05)
- **Issues**: [Report bugs or request features](https://github.com/AkshayRane05/PDF_Password_Cracker/issues)

---

⭐ **If this tool helped you understand PDF security better, please star the repository!**

## 📈 Related Projects

- [PDF Protection Tool](https://github.com/AkshayRane05/PDF_Protection_Tool) - Create password-protected PDFs
<!-- - [PDF Merger](https://github.com/AkshayRane05/PDF_Merger) - Combine multiple PDF files
- [Document Security Scanner](https://github.com/AkshayRane05/Doc_Security_Scanner) - Analyze document security -->
