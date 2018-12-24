# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, abort, make_response
from flask_login import login_required, current_user

from bluelog.emails import send_new_comment_email, send_new_reply_email
from bluelog.extensions import db
from bluelog.forms import ThreadForm, StressLifeForm
from bluelog.models import Post, Category, Comment
from bluelog.utils import redirect_back
from bluelog.funcs.thread_external_mj import thread_external_mj
from bluelog.funcs import global_var

data_bp = Blueprint('data', __name__)


@data_bp.route('/', methods=['GET', 'POST'])
def index():
    form = ThreadForm()
    progress_done = True
    if form.validate_on_submit():
        d = form.d.data
        P = form.P.data
        L = form.L.data
        n = form.n.data
        m = form.m.data
        seg = form.seg.data
        bound = form.bound.data
        # flash('Setting updated.', 'success')
        file_directory = current_app.config['DOWNLOAD_FOLDER']
        filename, progress_done = thread_external_mj(file_directory=file_directory, d=d, P=P, L=L, n=n, m=m, seg=seg, bound=bound)
        return redirect(url_for('data.index'))
    return render_template('data/index.html', form=form, progress_done=progress_done)


@data_bp.route('/show_progress')
def show_progress():
    return str(global_var.progress_percent)


@data_bp.route('/about')
@login_required
def about():
    return render_template('data/about.html')


@data_bp.route('/test')
def test():
    return render_template('data/test.html')

@data_bp.route('/stresslife', methods=['GET', 'POST'])
def stresslife():
    form = StressLifeForm()
    if form.validate_on_submit():
        if form.submit.data:  # 保存按钮被单击
            form.material_name.data = form.loadmatid.data
        elif form.loadmaterial.data:  # 发布按钮被单击
            form.material_name.data = 'IN718'
        return render_template('data/stresslife.html', form=form)
    return render_template('data/stresslife.html', form=form)