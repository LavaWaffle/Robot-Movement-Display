#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import libraries
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
import os
import pandas as pd
import warnings

# Turn on development mode
DEVELOPMENT_ENV  = True

# Create flask app
app = Flask(__name__)

# Set secret key
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

# Add bootstrap
Bootstrap(app)

# Form for xlsx file upload
class XlsxForm(FlaskForm):
    xlsx_file = FileField('File', validators=[FileRequired(), FileAllowed(['xlsx'], 'Only xlsx files are allowed!')])
    submit = SubmitField('Submit')

# Route for index page
@app.route('/' , methods=['GET', 'POST'])
def index():
    # Create form
    form = XlsxForm()
    # Create message
    message = {}
    # Check if form is submitted and valid
    if form.validate_on_submit():
        # Form is submitted and valid
        # Get the file from the request
        f = form.xlsx_file.data
        filename = secure_filename(f.filename)
        # Save the file to the uploads folder
        f.save(os.path.join(
            app.instance_path, 'uploads', filename
        ))
        # Redirect the user to a new page with a parameter of the file name
        return redirect(url_for('draw_xlsx', filename=filename))
    else:
        # Form is not submitted or not valid
        if form.errors:
            f = form.xlsx_file.data
            filename = secure_filename(f.filename)
            if (len(filename)!=0):
                # Form is not valid
                # Tell user form is not valid
                message = form.errors  
 
    # Render the template
    return render_template('index.html', form=form, message=message)

# Route for the viewing page
@app.route('/draw_xlsx/<filename>')
def draw_xlsx(filename):
    # Grab file_path from uploads folder
    file_path = os.path.join(app.instance_path, 'uploads', filename)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        # Read the file
        xlsx_file = pd.read_excel(file_path)
        # Convert from pandas object to python dictionary
        xlsx_file = xlsx_file.to_dict('list')
     
    
        # Render the template
        return render_template('draw_xlsx.html',  xlsx_file=xlsx_file, filename=filename)
    # Fall back render if read fails
    return render_template('draw_xlsx.html')

# If this file is the main file being run
if __name__ == '__main__':
    # Run the app
    app.run(debug=DEVELOPMENT_ENV)