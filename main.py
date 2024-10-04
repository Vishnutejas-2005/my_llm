from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import  SubmitField, SelectField, DateField, TextAreaField,StringField, PasswordField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError
from datetime import date
from wtforms.widgets import ListWidget, CheckboxInput
from flask_bootstrap import Bootstrap5  # pip install bootstrap-flask

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class LoginForm(FlaskForm):
    product = SelectField('Product', choices=[('rupay', 'Rupay')], validators=[DataRequired()])
    start_date = DateField('Start Date (yyyy-mm-dd)', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date (yyyy-mm-dd)', format='%Y-%m-%d', validators=[DataRequired()])
    filters = MultiCheckboxField('Filters', choices=[('approved_transactions', 'Approved transactions'), ('credit_cards', 'Credit cards')], validators=[DataRequired()])
    dimensions = SelectField('Dimensions', choices=[('month', 'Month'), ('issuing_bank', 'Issuing bank')], validators=[DataRequired()])
    metrics = SelectField('Metrics', choices=[('volume', 'Volume'), ('value', 'Value')], validators=[DataRequired()])
    comments = TextAreaField('Any other comments')
    submit = SubmitField(label="Log In")

    def validate_end_date(form, field):
        if field.data > date.today():
            raise ValidationError("End date must be today or in the past.")
        if form.start_date.data and field.data < form.start_date.data:
            raise ValidationError("End date must be after start date.")
        
app = Flask(__name__)
app.secret_key = "any-string-you-want-just-keep-it-secret"
bootstrap = Bootstrap5(app)

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        product = login_form.product.data.title()
        # Format the date to dd-mm-yyyy
        start_date = login_form.start_date.data.strftime('%d-%m-%Y')
        end_date = login_form.end_date.data.strftime('%d-%m-%Y')
        filters = [filter_.title() for filter_ in login_form.filters.data]  # Handle multiple checkboxes
        dimensions = login_form.dimensions.data.title()
        metrics = login_form.metrics.data.title()
        comments = login_form.comments.data

        # For now, just print the additional fields to the console (or handle them as needed)
        print(f"Product: {product}")
        print(f"Time window: {start_date} to {end_date}")
        print(f"Filters: {', '.join(filters)}")
        print(f"Dimensions: {dimensions}")
        print(f"Metrics: {metrics}")
        if comments:
            print(f"Comments: {comments}")
        return render_template("success.html", product=product, start_date=start_date, end_date=end_date, filters=', '.join(filters), dimensions=dimensions, metrics=metrics, comments=comments)
        
    return render_template("login.html", form=login_form)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
