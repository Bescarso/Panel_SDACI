# 🔧 Panel_SDACI App

**Panel_SDACI** is a desktop application designed for the **maintenance department** working with **Simplex fire alarm systems**. It allows users to **search devices by address**, view their **maintenance history**, and perform **maintenance tracking operations**.

---

## 🖼️ Images

Below are some screenshots and images from the `images` folder illustrating the app interface:

<img src="images/image1.png" alt="Image 1" width="300"/>
<img src="images/image2.png" alt="Image 2" width="300"/>
---

## ✨ Features

- 🔍 **Search devices** by address (`address_device`)
- 🕒 **View maintenance history** with detailed information
- ➕ **Add new maintenance records**
- ❌ **Delete history entries**
- 💾 **Store all data in a SQL Server database**

---

## 🧱 Architecture

The system is composed of:

1. 🖼️ **GUI (Flet)**: Modern, responsive UI built with [Flet](https://flet.dev), a Python-based Flutter-style framework.
2. 🗄️ **Database (SQL Server)**: Local or cloud-hosted SQL Server for persistent storage of device and maintenance data.

---

## 🐍 Dependencies

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```
---

## 🚀 Running the Application

### As a Desktop App:

```bash
flet run src/main.py
```

---

## 📬 Contact

For questions or feedback, contact at `billysoplin@gmail.com`

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---


