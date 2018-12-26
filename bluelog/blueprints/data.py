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
from bluelog.forms import ThreadForm, StressLifeForm, PostForm, ExperimentForm
from bluelog.models import Post, Category, Comment, Experiment
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


@data_bp.route('/datatable')
@login_required
def datatable():
    return render_template('data/datatable.html')


@data_bp.route('/form')
def form():
    return render_template('data/edit_post.html')


@data_bp.route('/experiment/new', methods=['GET', 'POST'])
# @login_required
def new_experiment():
    form = ExperimentForm()
    if form.validate_on_submit():
        specimen = form.specimen.data
        user = form.user.data
        extensometer = form.extensometer.data
        body = form.body.data
        category = Category.query.get(form.category.data)
        experiment = Experiment(specimen=specimen, user=user, extensometer=extensometer, body=body, category=category)
        # same with:
        # category_id = form.category.data
        # post = Post(title=title, body=body, category_id=category_id)
        db.session.add(experiment)
        db.session.commit()
        flash('Post created.', 'success')
        return redirect(url_for('data.datatable'))
    return render_template('data/edit_post.html', form=form)


@data_bp.route('/experiment/<int:experiment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_experiment(experiment_id):
    form = ExperimentForm()
    experiment = Experiment.query.get_or_404(experiment_id)
    if form.validate_on_submit():
        experiment.specimen = form.specimen.data
        experiment.user = form.user.data
        experiment.extensometer = form.extensometer.data
        experiment.body = form.body.data
        experiment.category = Category.query.get(form.category.data)
        db.session.commit()
        flash('Post updated.', 'success')
        return redirect(url_for('data.datatable'))
    form.specimen.data = experiment.specimen
    form.user.data = experiment.user
    form.extensometer.data = experiment.extensometer
    form.body.data = experiment.body
    form.category.data = experiment.category_id
    return render_template('data/edit_post.html', form=form)


@data_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', 'success')
    return redirect_back()


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