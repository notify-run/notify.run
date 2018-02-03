self.addEventListener('push', function (event) {
    let data = event.data.json();
    const promiseChain = self.registration.showNotification(data.message, {
        icon: '/icon.png',
        tag: data.channel,
        renotify: true,
    });

    event.waitUntil(promiseChain);
});