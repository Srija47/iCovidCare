from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, TextField
from wtforms.validators import DataRequired, Length, Email


class SearchForm(FlaskForm):
    search_input = StringField('Search Doctor', validators=[DataRequired(), Length(max=60)])
    submit=SubmitField('submit')


class ContactForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)],
                           render_kw={"placeholder":"Username"})
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder":"Email"})
    subject = TextField("Subject",validators=[DataRequired()],render_kw={"placeholder":"Subject"})
    message = TextAreaField("Message",validators=[DataRequired()],render_kw={"placeholder":"Message"})
    submit = SubmitField("Send")
