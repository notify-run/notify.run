self.addEventListener('notificationclick', function (event) {
    if (event.notification.data.action) {
        clients.openWindow(event.notification.data.action);
    }
});

self.addEventListener('push', function (event) {
    let data = event.data.json();

    let title_body = data.message.split('\n');
    let title = title_body.shift();
    let body = title_body.join('\n');

    let options = {
        body: body,
        icon: '/icon.png',
        tag: data.channel,
        data: data.data,
        renotify: true,
        vibrate: data.vibrate,
        silent: data.silent
    };

    console.log(JSON.stringify(event.data.json()))
    console.log(JSON.stringify(options))

    const promiseChain = self.registration.showNotification(title, options);

    event.waitUntil(promiseChain);
});