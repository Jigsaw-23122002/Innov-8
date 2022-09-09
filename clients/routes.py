from urllib import request
from supabase import create_client, Client
from flask import redirect, render_template, flash
from clients import app
from clients.forms import LoginForm, SignUpForm

supabase: Client = create_client("https://yuhrnfjyvvbluvhlpbhm.supabase.co",
                                 "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl1aHJuZmp5dnZibHV2aGxwYmhtIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NjIyOTQzOTYsImV4cCI6MTk3Nzg3MDM5Nn0.ueJAWAmBuCAE4wvCvSihgiWcS73S8hsbT0CiiICRhdo")

@app.route('/')
def home_page():
    # if supabase.auth.current_user:
    #     print(supabase.auth.current_user.id)
    # else:
    #     print('null')
    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        try:
            random_email: str = form.email.data
            random_password: str = form.password.data
            user = supabase.auth.sign_up(
                email=random_email, password=random_password)
            # if supabase.auth.current_user:
            #     print(supabase.auth.current_user.id)
            # else:
            #     print('null')
            return redirect('/login')

        except ValueError as e:
            print('An exception occured')

    if form.errors != {}:
        for err in form.errors.values():
            flash(
                f'there was an error in creating a user:{err}', category="danger")

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            random_email: str = form.email.data
            random_password: str = form.password.data
            user = supabase.auth.sign_in(
                email=random_email, password=random_password)
            # print(supabase.auth.current_user.id)
            return redirect('/')

        except ValueError as e:
            print(e)

    return render_template('login.html', form=form)


@app.route('/individual_projects')
def individual_projects():
    # Fetch the projects made the uuid of the student who is signed in
    data = [{
        'project_uuid': 'lambda',
        'team_name': 'TechnoSrats',
            'team_members': [
                'Harsh Nag',
                'Sarvagnya Purohit',
                'Ketaki Deshmukh',
                'Smit Sekhadia',
                'Anuraag Jajoo'
            ],
            'project_description':'This template offers an outline to create an architectural or construction project description template. Customize the template based on the type of project and the needs of your company or client. List supporting documents, such as environmental analysis or additional design plans. Follow the template format to create a thorough project description that includes goals, phases, design specifications, and financial requirements.'
            }, {
            'project_uuid': 'lambda',
            'team_name': 'TechnoSrats',
            'team_members': [
                'Harsh Nag',
                'Sarvagnya Purohit',
                'Ketaki Deshmukh',
                'Smit Sekhadia',
                'Anuraag Jajoo'
            ],
            'project_description':'This template offers an outline to create an architectural or construction project description template. Customize the template based on the type of project and the needs of your company or client. List supporting documents, such as environmental analysis or additional design plans. Follow the template format to create a thorough project description that includes goals, phases, design specifications, and financial requirements.'
            }, {
            'project_uuid': 'lambda',
            'team_name': 'TechnoSrats',
            'team_members': [
                'Harsh Nag',
                'Sarvagnya Purohit',
                'Ketaki Deshmukh',
                'Smit Sekhadia',
                'Anuraag Jajoo'
            ],
            'project_description':'This template offers an outline to create an architectural or construction project description template. Customize the template based on the type of project and the needs of your company or client. List supporting documents, such as environmental analysis or additional design plans. Follow the template format to create a thorough project description that includes goals, phases, design specifications, and financial requirements.'
            }, {
            'project_uuid': 'lambda',
            'team_name': 'TechnoSrats',
            'team_members': [
                'Harsh Nag',
                'Sarvagnya Purohit',
                'Ketaki Deshmukh',
                'Smit Sekhadia',
                'Anuraag Jajoo'
            ],
            'project_description':'This template offers an outline to create an architectural or construction project description template. Customize the template based on the type of project and the needs of your company or client. List supporting documents, such as environmental analysis or additional design plans. Follow the template format to create a thorough project description that includes goals, phases, design specifications, and financial requirements.'
            }
            ]
    return render_template('individual_projects.html', data=data)


@app.route('/individual_events')
def individual_events():
    # Fetch the projects made the uuid of the organizer who is signed in
    data = [{
        'event_uuid': 'sunderbans',
        'event_name': 'HackOdisha 2.0',
        'event_sponsorers': [
            'Amazon',
            'Flipkart',
            'Firebase'
        ],
        'event_description':'An event description is copy that aims to tell your potential attendees what will be happening at the event, who will be speaking, and what they will get out of attending. Good event descriptions can drive attendance to events and also lead to more media coverage.',
    }, {
        'event_uuid': 'sunderbans',
        'event_name': 'HackOdisha 2.0',
        'event_sponsorers': [
            'Amazon',
            'Flipkart',
            'Firebase'
        ],
        'event_description':'An event description is copy that aims to tell your potential attendees what will be happening at the event, who will be speaking, and what they will get out of attending. Good event descriptions can drive attendance to events and also lead to more media coverage.',
    }, {
        'event_uuid': 'sunderbans',
        'event_name': 'HackOdisha 2.0',
        'event_sponsorers': [
            'Amazon',
            'Flipkart',
            'Firebase'
        ],
        'event_description':'An event description is copy that aims to tell your potential attendees what will be happening at the event, who will be speaking, and what they will get out of attending. Good event descriptions can drive attendance to events and also lead to more media coverage.',
    }, {
        'event_uuid': 'sunderbans',
        'event_name': 'HackOdisha 2.0',
        'event_sponsorers': [
            'Amazon',
            'Flipkart',
            'Firebase'
        ],
        'event_description':'An event description is copy that aims to tell your potential attendees what will be happening at the event, who will be speaking, and what they will get out of attending. Good event descriptions can drive attendance to events and also lead to more media coverage.',
    }]
    return render_template('individual_events.html', data=data)


@app.route('/list_projects')
def list_projects():
    # Fetch the list of projects for the particular event
    data = [{
        'project_uuid': 'lambda',
        'team_name': 'TechnoSrats',
            'team_members': [
                'Harsh Nag',
                'Sarvagnya Purohit',
                'Ketaki Deshmukh',
                'Smit Sekhadia',
                'Anuraag Jajoo'
            ],
            'project_description':'This template offers an outline to create an architectural or construction project description template. Customize the template based on the type of project and the needs of your company or client. List supporting documents, such as environmental analysis or additional design plans. Follow the template format to create a thorough project description that includes goals, phases, design specifications, and financial requirements.'
            }, {
            'project_uuid': 'lambda',
            'team_name': 'TechnoSrats',
            'team_members': [
                'Harsh Nag',
                'Sarvagnya Purohit',
                'Ketaki Deshmukh',
                'Smit Sekhadia',
                'Anuraag Jajoo'
            ],
            'project_description':'This template offers an outline to create an architectural or construction project description template. Customize the template based on the type of project and the needs of your company or client. List supporting documents, such as environmental analysis or additional design plans. Follow the template format to create a thorough project description that includes goals, phases, design specifications, and financial requirements.'
            }, {
            'project_uuid': 'lambda',
            'team_name': 'TechnoSrats',
            'team_members': [
                'Harsh Nag',
                'Sarvagnya Purohit',
                'Ketaki Deshmukh',
                'Smit Sekhadia',
                'Anuraag Jajoo'
            ],
            'project_description':'This template offers an outline to create an architectural or construction project description template. Customize the template based on the type of project and the needs of your company or client. List supporting documents, such as environmental analysis or additional design plans. Follow the template format to create a thorough project description that includes goals, phases, design specifications, and financial requirements.'
            }, {
            'project_uuid': 'lambda',
            'team_name': 'TechnoSrats',
            'team_members': [
                'Harsh Nag',
                'Sarvagnya Purohit',
                'Ketaki Deshmukh',
                'Smit Sekhadia',
                'Anuraag Jajoo'
            ],
            'project_description':'This template offers an outline to create an architectural or construction project description template. Customize the template based on the type of project and the needs of your company or client. List supporting documents, such as environmental analysis or additional design plans. Follow the template format to create a thorough project description that includes goals, phases, design specifications, and financial requirements.'
            }
            ]
    return render_template('list_of_projects.html', data=data)


@app.route('/list_events')
def list_events():
    # Fetch the list of events available for participation
    data = [{
        'event_uuid': 'sunderbans',
        'event_name': 'HackOdisha 2.0',
        'event_sponsorers': [
            'Amazon',
            'Flipkart',
            'Firebase'
        ],
        'event_description':'An event description is copy that aims to tell your potential attendees what will be happening at the event, who will be speaking, and what they will get out of attending. Good event descriptions can drive attendance to events and also lead to more media coverage.',
    }, {
        'event_uuid': 'sunderbans',
        'event_name': 'HackOdisha 2.0',
        'event_sponsorers': [
            'Amazon',
            'Flipkart',
            'Firebase'
        ],
        'event_description':'An event description is copy that aims to tell your potential attendees what will be happening at the event, who will be speaking, and what they will get out of attending. Good event descriptions can drive attendance to events and also lead to more media coverage.',
    }, {
        'event_uuid': 'sunderbans',
        'event_name': 'HackOdisha 2.0',
        'event_sponsorers': [
            'Amazon',
            'Flipkart',
            'Firebase'
        ],
        'event_description':'An event description is copy that aims to tell your potential attendees what will be happening at the event, who will be speaking, and what they will get out of attending. Good event descriptions can drive attendance to events and also lead to more media coverage.',
    }, {
        'event_uuid': 'sunderbans',
        'event_name': 'HackOdisha 2.0',
        'event_sponsorers': [
            'Amazon',
            'Flipkart',
            'Firebase'
        ],
        'event_description':'An event description is copy that aims to tell your potential attendees what will be happening at the event, who will be speaking, and what they will get out of attending. Good event descriptions can drive attendance to events and also lead to more media coverage.',
    }]
    return render_template('list_of_events.html', data=data)

@app.route('/logout')
def logout():
    supabase.auth.sign_out()
    return redirect('/')