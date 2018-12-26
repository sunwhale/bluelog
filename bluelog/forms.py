# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, HiddenField, \
    BooleanField, PasswordField, IntegerField, FloatField
from wtforms.validators import DataRequired, Email, Length, Optional, URL, NumberRange

from bluelog.models import Category


class LoginForm(FlaskForm):
    username = StringField(u'用户名:', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField(u'密码:', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField(u'记住我')
    submit = SubmitField(u'登陆')


class SettingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 70)])
    blog_title = StringField('Blog Title', validators=[DataRequired(), Length(1, 60)])
    blog_sub_title = StringField('Blog Sub Title', validators=[DataRequired(), Length(1, 100)])
    about = CKEditorField('About Page', validators=[DataRequired()])
    submit = SubmitField()


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('Category', coerce=int, default=1)
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('Name already in use.')


class CommentForm(FlaskForm):
    author = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
    site = StringField('Site', validators=[Optional(), URL(), Length(0, 255)])
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField()


class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()


class LinkForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    url = StringField('URL', validators=[DataRequired(), URL(), Length(1, 255)])
    submit = SubmitField()


class ThreadForm(FlaskForm):
    d = FloatField('d =', default=10.0, validators=[DataRequired(), NumberRange(min=None, max=None)])
    P = FloatField('P =', default=1.25, validators=[DataRequired(), NumberRange(min=None, max=None)])
    L = FloatField('L =', default=1.25, validators=[DataRequired(), NumberRange(min=None, max=None)])
    n = IntegerField('n =', default=16, validators=[DataRequired(), NumberRange(min=None, max=64)])
    m = IntegerField('m =', default=16, validators=[DataRequired(), NumberRange(min=None, max=64)])
    seg = IntegerField('seg =', default=5, validators=[DataRequired(), NumberRange(min=None, max=20)])
    bound = IntegerField('bound =', default=2, validators=[DataRequired(), NumberRange(min=None, max=5)])
    submit = SubmitField('Create')


class StressLifeForm(FlaskForm):
    maximum = FloatField('Maximum', default=100.0, validators=[DataRequired(), NumberRange(min=None, max=None)])
    minimum = FloatField('Minimum', default=100.0, validators=[DataRequired(), NumberRange(min=None, max=None)])
    alternating = FloatField('Alternating', default=100.0, validators=[DataRequired(), NumberRange(min=None, max=None)])
    mean = FloatField('Mean', default=100.0, validators=[DataRequired(), NumberRange(min=None, max=None)])
    material_name = StringField('Material Name', validators=[Length(0, 128)])
    loadmaterial = SubmitField('Load Material')
    submit = SubmitField('Create')
    loadmatid = SelectField(
        label='Material ID',
        render_kw={
            'class': 'form-control',
        },
        choices=[(1, ''), (2, 'mat1')],
        coerce=int,
        default=1
    )


class ExperimentForm(FlaskForm):
    specimen = IntegerField('specimen')
    user = StringField('user', validators=[DataRequired(), Length(1, 30)])
    extensometer = StringField('extensometer', validators=[DataRequired(), Length(1, 30)])
    category = SelectField('Category', coerce=int, default=1)
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(ExperimentForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]