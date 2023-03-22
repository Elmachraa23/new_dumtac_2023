from app.site import blueprint
import logging

from flask import render_template


@blueprint.route('/accueil')
def page_accueil():
    return render_template("index.html", current_page='page_accueil')


@blueprint.route('/about')
def about_page():
    return render_template("about.html", current_page='page_accueil')

@blueprint.route('/portfolio')
def portfolio_page():
    return render_template("portfolio.html", current_page='portfolio_page')

@blueprint.route('/portfolio_BM')
def pt_bluemedical_page():
    return render_template("blueMedical.html")

@blueprint.route('/contact')
def contact_page():
    return render_template("contact.html", current_page='render_template')