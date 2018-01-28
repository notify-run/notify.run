self.addEventListener('push', function (event) {
    const promiseChain = self.registration.showNotification(event.data.text(), {
        icon: '/icon.png',
    });

    event.waitUntil(promiseChain);
});