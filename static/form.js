const response = fetch(url,{
    method: 'POST',
    headers: {
        'X-CSRF-Token': document.getElementById('csrf_token').value,
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams(new FormData(form))
})