from flask import Blueprint, jsonify, current_app, render_template
from models import db, Psychologist
from helpers import add_or_update_psychologist 
from scraper import (
    get_psychologist_names_from_avtale, 
    scrape_privatpraktiserende, 
    scrape_legelisten
)



routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return render_template('index.html')


@routes.route('/scrape_avtalespesialister')
def scrape_avtalespesialister_route():
    url = 'https://avtalespesialister.helse-sorost.no/Spesialister1.asp?cmd=Detail&type=351&id=3'
    scraped_names = get_psychologist_names_from_avtale(url)
    
    if scraped_names:  # Sjekk om listen ikke er tom
        for name in scraped_names:
            psychologist = Psychologist(name=name, status='avtalespesialist')
            db.session.add(psychologist)
        db.session.commit()
        return jsonify({"status": "success", "added_names": len(scraped_names)})
    else:
        return jsonify({"status": "error", "message": "No psychologists found"})

@routes.route('/scrape_privatpraktiserende')
def scrape_privatpraktiserende_route():
    url = 'https://finnenpsykolog.no/searchres/?field=&wf=&srch_bk=&qr=&serch='
    scraped_names = scrape_privatpraktiserende(url)

    for name in scraped_names:
        if not Psychologist.query.filter_by(name=name).first():
            psychologist = Psychologist(name=name)
            db.session.add(psychologist)

    db.session.commit()
    return jsonify({"status": "success", "added_names": len(scraped_names)})

@routes.route('/scrape_legelisten')
def scrape_legelisten_route():
    base_url = 'https://www.legelisten.no/psykologer/Oslo?side='
    scraped_psychologists = scrape_legelisten(base_url)
    for psychologist_info in scraped_psychologists:
        add_or_update_psychologist(psychologist_info)  # Sørg for at denne funksjonen finnes
    db.session.commit()
    return jsonify({"status": "success", "added_names": len(scraped_psychologists)})
