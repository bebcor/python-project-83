import os
from urllib.parse import urlparse

import requests
import validators
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)

from .database import init_db  # Убедитесь что init_db не требует аргументов
from .url_repository import (
    create_url,
    create_url_check,
    find_url_by_name,
    get_all_urls_with_checks,
    get_url_by_id,
    get_url_checks,
)

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

init_db()


def normalize_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}".lower()


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.route('/urls', methods=['POST'])
def add_url():
    url = request.form.get('url', '').strip()
    
    if not url:
        flash('URL обязателен', 'danger')
        return render_template('index.html'), 422
        
    if len(url) > 255:
        flash('URL превышает 255 символов', 'danger')
        return render_template('index.html'), 422
        
    if not validators.url(url):
        flash('Некорректный URL', 'danger')
        return render_template('index.html'), 422

    normalized_url = normalize_url(url)
    
    try:
        existing_url = find_url_by_name(normalized_url)
        
        if existing_url:
            flash('Страница уже существует', 'info')
            url_id = existing_url[0]
        else:
            new_url = create_url(normalized_url)
            url_id = new_url[0]
            flash('Страница успешно добавлена', 'success')
            
        return redirect(url_for('show_url', id=url_id))
        
    except Exception as e:
        app.logger.error(f'Database error: {str(e)}')
        flash(f'Ошибка базы данных: {str(e)}', 'danger')
        return render_template('index.html'), 500


@app.route('/urls')
def list_urls():
    try:
        urls_data = get_all_urls_with_checks()
        formatted_urls = []
        for url in urls_data:
            formatted_urls.append({
                'id': url[0],
                'name': url[1],
                'last_check_date': url[2].strftime('%Y-%m-%d') 
                if url[2] else None,
                'last_check_status': url[3]
            })
        return render_template('urls.html', urls=formatted_urls)
    except Exception as e:
        app.logger.error(f'Error loading URLs: {str(e)}')
        flash(f'Ошибка при загрузке сайтов: {str(e)}', 'danger')
        return render_template('urls.html', urls=[]), 500


@app.route('/urls/<int:id>')
def show_url(id):
    try:
        url_row = get_url_by_id(id)
        
        if not url_row:
            flash('Страница не найдена', 'danger')
            return redirect(url_for('index'))
        
        url = {
            'id': url_row[0],
            'name': url_row[1],
            'created_at': url_row[2].strftime('%Y-%m-%d') if url_row[2] else ''
        }
        
        checks = get_url_checks(id)
        return render_template('url.html', url=url, checks=checks)
        
    except Exception as e:
        app.logger.error(f'Error loading URL {id}: {str(e)}')
        flash(f'Ошибка при загрузке страницы: {str(e)}', 'danger')
        return redirect(url_for('index'))


@app.route('/urls/<int:id>/checks', methods=['POST'])
def create_check(id):
    try:
        url_row = get_url_by_id(id)
        if not url_row:
            flash('Страница не найдена', 'danger')
            return redirect(url_for('index'))
        
        url_name = url_row[1]
        
        try:
            headers = {
                'User-Agent': (
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/58.0.3029.110 Safari/537.3'
                )       
            }
            
            response = requests.get(
                url_name, 
                headers=headers, 
                timeout=10, 
                allow_redirects=True
            )
            response.raise_for_status()
            
            if response.encoding is None:
                response.encoding = 'utf-8'
                
            status_code = response.status_code
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            h1 = soup.h1.get_text().strip() if soup.h1 else None
            title = soup.title.string.strip() if soup.title else None
            
            meta_description = soup.find('meta', attrs={'name': 'description'})
            description = (
                meta_description['content'].strip() 
                if meta_description and 'content' in meta_description.attrs 
                else None
            )
            
            create_url_check(id, status_code, h1, title, description)
            
            flash('Страница успешно проверена', 'success')
            
        except requests.exceptions.RequestException as e:
            app.logger.error(f'Ошибка при проверке URL {url_name}: {str(e)}')
            flash('Произошла ошибка при проверке', 'danger')
            
        except Exception as e:
            app.logger.error(
                f'Ошибка при обработке страницы {url_name}: {str(e)}'
            )
            flash('Произошла ошибка при анализе страницы', 'danger')
            
    except Exception as e:
        app.logger.error(f'Ошибка при создании проверки для URL {id}: {str(e)}')
        flash(f'Ошибка при создании проверки: {str(e)}', 'danger')
    
    return redirect(url_for('show_url', id=id))


@app.template_filter('truncate')
def truncate_filter(s, length=100):
    if s and len(s) > length:
        return s[:length] + '...'
    return s
