
# Conversie CAEN3 – Convertor coduri CAEN Rev.2 la Rev.3

🎯 Aplicație web interactivă creată cu [Streamlit](https://streamlit.io/) pentru conversia codurilor CAEN (Clasificarea Activităților din Economia Națională) din versiunea Rev.2 în versiunea Rev.3 – actualizat pentru anul 2024.

## 🌐 Acces online

👉 [https://conversie-caen3.ro](https://conversie-caen3.ro)

## ⚙️ Funcționalități

- Conversie instantă a codurilor CAEN din Rev.2 în Rev.3
- Căutare individuală sau în serie (bulk input)
- Export rezultate în Word sau Excel
- Navigare între mai multe secțiuni (Rev.3, convertor fișiere)
- Suport multilingv (RO / EN)
- UI modern și responsive
- Optimizat SEO (titlu, descriere, meta taguri, sitemap.xml, robots.txt)

## 🚀 Tehnologii folosite

- [Python 3.10+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- `pandas`, `openpyxl`, `python-docx`
- `beautifulsoup4` (pentru modificarea HTML-ului la runtime)
- Deploy pe [Render.com](https://render.com)

## 📁 Structură fișiere importante

- `app.py` – fișierul principal Streamlit
- `data_processor.py` – extragerea datelor din PDF
- `translations.py` – suport pentru RO / EN
- `robots.txt` – instrucțiuni pentru Googlebot
- `sitemap.xml` – hartă pentru indexare SEO

## 🔍 SEO și indexare

Pentru a îmbunătăți prezența în Google:

- Meta tag-urile pentru SEO sunt injectate în `index.html` la runtime, folosind `BeautifulSoup`
- Fișierele `robots.txt` și `sitemap.xml` sunt plasate în directorul principal și servite automat
- Titlul și descrierea sunt setate atât în `<head>`, cât și în conținutul vizibil (pentru fallback)
- Integrarea completă este compatibilă cu deploy pe Render

## 🧪 Testare locală

```bash
pip install -r requirements.txt
streamlit run app.py
```

## ✅ Acces fișiere SEO (public)

- [https://conversie-caen3.ro/robots.txt](https://conversie-caen3.ro/robots.txt)
- [https://conversie-caen3.ro/sitemap.xml](https://conversie-caen3.ro/sitemap.xml)

---

## 🧑‍💻 Autor

Creat de **Panghe Tiberiu-Andrei**  
🔗 [github.com/TiberiuP7](https://github.com/TiberiuP7) – 2024  
Sugestii sau feedback? Deschide un issue sau trimite un PR! 🚀
