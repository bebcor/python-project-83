## 📈 Page Analyzer
[![Actions Status](https://github.com/bebcor/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/bebcor/python-project-83/actions)
[![Maintainability](https://qlty.sh/badges/be526e2f-2773-4aa9-a995-86174c2d9f5a/maintainability.svg)](https://qlty.sh/gh/bebcor/projects/python-project-83)
[![CI](https://github.com/bebcor/python-project-83/actions/workflows/pyci.yml/badge.svg)](https://github.com/bebcor/python-project-83/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=bebcor_python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=bebcor_python-project-83)

**Page Analyzer** is a web application on Flask for analyzing the SEO suitability of web pages. The application checks the availability of the site, extracts and analyzes key HTML elements (title, h1, description), checks the status of the server response and allows you to save the history of checks.

### 💻 Technology stack
|     Tools      | Version |
|:--------------:|:-------:|
|     Python     | ^3.13.0 |
|     Flask      | ^3.1.0  |
|     gunicorn   | ^23.0.0 |
| python-dotenv  | ^1.1.0  |
|     ruff       | ^0.11.4 |
| psycopg2-binary| ^2.9.10 |
| beautifulsoup4 | ^4.13.4 |
|     requests   | ^2.32.4 |
|     validators | ^0.35.0 |

### ⏳ Installation  & Launching

1. Install dependencies:
   
```bash
make install
```

2. Launch during development

```bash
make dev
```

3. Linter
   
```bash
 make lint
```

4. Build & Run the application:
   
```bash
make build
make start-server
```

### ❤️ Acknowledgements
Thanks for stopping by, buddy! If you find this tool helpful, don't forget to give it a ⭐ on GitHub!

