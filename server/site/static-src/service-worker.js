self.addEventListener('push', function (event) {
    let data = event.data.json();

    let title_body = data.message.split('\n');
    let title = title_body.shift();
    let body = title_body.join('\n');

    const promiseChain = self.registration.showNotification(title, {
        body: body,
        icon: '/icon.png',
        tag: data.channel,
        renotify: true,
    });

    event.waitUntil(promiseChain);
});