from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------- Model ----------
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000))
    start_time = db.Column(db.DateTime, nullable=False)  # full datetime
    end_time = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(100))

    def to_event(self):
        # FullCalendar event representation for the actual timed event
        color = None  # let the calendar use default unless you want category colors
        return {
            "id": self.id,
            "title": f"{self.title} ({self.category})" if self.category else self.title,
            "start": self.start_time.isoformat(),
            "end": self.end_time.isoformat(),
            "allDay": False,
            "extendedProps": {
                "description": self.description or "",
                "category": self.category or ""
            },
            "backgroundColor": color
        }

# ---------- Routes - pages ----------
@app.route('/')
def home():
    return redirect(url_for('calendar_view'))

@app.route('/calendar')
def calendar_view():
    return render_template('calendar.html')

@app.route('/tasks')
def tasks_view():
    tasks = Task.query.order_by(Task.start_time).all()
    return render_template('tasks.html', tasks=tasks)

# Create new task (from either page)
@app.route('/tasks/create', methods=['POST'])
def create_task():
    title = request.form.get('title')
    description = request.form.get('description')
    start = request.form.get('start')  # expecting 'YYYY-MM-DDTHH:MM'
    end = request.form.get('end')
    category = request.form.get('category')

    if not (title and start and end):
        abort(400, "title/start/end required")

    # parse datetime-local input
    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)
    if end_dt < start_dt:
        abort(400, "end must be after start")

    new_task = Task(title=title, description=description, start_time=start_dt, end_time=end_dt, category=category)
    db.session.add(new_task)
    db.session.commit()
    return redirect(request.referrer or url_for('tasks_view'))

# Edit task
@app.route('/tasks/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        task.start_time = datetime.fromisoformat(request.form.get('start'))
        task.end_time = datetime.fromisoformat(request.form.get('end'))
        task.category = request.form.get('category')
        db.session.commit()
        return redirect(url_for('tasks_view'))
    # GET: render a simple edit form inline on tasks page — we'll reuse tasks view with anchor
    tasks = Task.query.order_by(Task.start_time).all()
    return render_template('tasks.html', tasks=tasks, edit_task=task)

# Delete
@app.route('/tasks/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(request.referrer or url_for('tasks_view'))

# ---------- API for calendar ----------
@app.route('/api/events')
def api_events():
    """
    Returns:
    - actual events with start/end (for calendar rendering)
    - background (all-day) markers for dates that have at least one event (to color the date cell)
    Optional query param: date=YYYY-MM-DD to return just events for that day (used for modal listing)
    """
    qdate = request.args.get('date')
    tasks = Task.query.all()

    events = [t.to_event() for t in tasks]

    if qdate:
        # filter events that intersect that date
        try:
            d = datetime.fromisoformat(qdate).date()
        except ValueError:
            d = datetime.strptime(qdate, "%Y-%m-%d").date()
        day_events = []
        for t in tasks:
            # if the event overlaps the day d
            if (t.start_time.date() <= d <= t.end_time.date()):
                day_events.append({
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "start": t.start_time.isoformat(),
                    "end": t.end_time.isoformat(),
                    "category": t.category
                })
        return jsonify(day_events)

    # create background markers (one per date that has at least one event)
    marked_dates = set()
    for t in tasks:
        cur = t.start_time.date()
        last = t.end_time.date()
        while cur <= last:
            marked_dates.add(cur.isoformat())
            cur = cur + timedelta(days=1)

    # background events to highlight dates (FullCalendar supports display:'background')
    for d in marked_dates:
        events.append({
            "id": f"bg-{d}",
            "title": "",
            "start": d,
            "end": d,
            "allDay": True,
            "display": "background",
            "backgroundColor": "yellow",
            "borderColor": "yellow"
        })

    return jsonify(events)

# ---------- boot ----------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0',debug=True,port=5001)



        
    
