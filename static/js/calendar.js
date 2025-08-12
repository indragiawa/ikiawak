document.addEventListener('DOMContentLoaded', function () {
  var calendarEl = document.getElementById('calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    height: 'auto',
    events: '/api/events', // returns events + background markers
    eventClick: function(info) {
      // show event details in modal
      var evt = info.event;
      // if it's a background marker, do nothing
      if(evt.display === 'background') return;

      var title = evt.title;
      var desc = evt.extendedProps.description || '';
      var category = evt.extendedProps.category || '';
      var start = evt.start ? evt.start.toLocaleString() : '';
      var end = evt.end ? evt.end.toLocaleString() : '';

      var html = '<h5>' + title + '</h5>';
      if(category) html += '<div><strong>Kategori:</strong> ' + category + '</div>';
      html += '<div><strong>Waktu:</strong> ' + start + ' — ' + end + '</div>';
      if(desc) html += '<div class="mt-2"><strong>Deskripsi:</strong><br>' + desc + '</div>';

      var modalBody = document.getElementById('modalBody');
      modalBody.innerHTML = html;
      document.getElementById('modalDate').innerText = evt.start.toLocaleDateString();
      var eventsModal = new bootstrap.Modal(document.getElementById('eventsModal'));
      eventsModal.show();
    },
    dateClick: function(info) {
      // fetch events for this date then show in modal
      var clickedDate = info.dateStr; // YYYY-MM-DD
      fetch('/api/events?date=' + clickedDate)
        .then(res => res.json())
        .then(data => {
          var html = '';
          if(data.length === 0) {
            html = '<div class="text-muted">Tidak ada kegiatan pada hari ini.</div>';
          } else {
            data.forEach(function(e){
              html += '<div class="card mb-2"><div class="card-body">';
              html += '<h6>' + e.title + '</h6>';
              if(e.category) html += '<div><small class="text-muted">' + e.category + '</small></div>';
              html += '<div><small>' + (new Date(e.start)).toLocaleString() + ' — ' + (new Date(e.end)).toLocaleString() + '</small></div>';
              if(e.description) html += '<div class="mt-2">' + e.description + '</div>';
              html += '<div class="mt-2"><a class="btn btn-sm btn-outline-primary" href="/tasks">Lihat/Edit</a></div>';
              html += '</div></div>';
            });
          }
          document.getElementById('modalBody').innerHTML = html;
          document.getElementById('modalDate').innerText = clickedDate;
          var eventsModal = new bootstrap.Modal(document.getElementById('eventsModal'));
          eventsModal.show();
        });
    },
    // make background markers 'behind' events
    eventDisplay: 'auto',
  });

  calendar.render();
});

