/*

=========================================================
* Volt - Bootstrap 5 Admin Dashboard
=========================================================

* Product Page: https://themesberg.com/product/admin-dashboard/volt-bootstrap-5-dashboard
* Copyright 2020 Themesberg (https://www.themesberg.com)

* Designed and coded by https://themesberg.com

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. Please contact us to request a removal.

*/

"use strict";
const d = document;
d.addEventListener("DOMContentLoaded", function (event) {

    // options
    const breakpoints = {
        sm: 540,
        md: 720,
        lg: 960,
        xl: 1140
    };

    var preloader = d.querySelector('.preloader');
    if (preloader) {
        setTimeout(function () {
            preloader.classList.add('show');

            setTimeout(function () {
                d.querySelector('.loader-element').classList.add('hide');
            }, 200);
        }, 1000);
    }

    var iconNotifications = d.querySelector('.icon-notifications');
    if (iconNotifications) {
        var unreadNotifications = d.querySelector('.unread-notifications');
        var bellShake = d.querySelector('.bell-shake');

        if (iconNotifications.getAttribute('data-unread-notifications') === 'true') {
            unreadNotifications.style.display = 'block';
        } else {
            unreadNotifications.style.display = 'none';
        }

        // bell shake
        var shakingInterval = setInterval(function () {
            if (iconNotifications.getAttribute('data-unread-notifications') === 'true') {
                if (bellShake.classList.contains('shaking')) {
                    bellShake.classList.remove('shaking');
                } else {
                    bellShake.classList.add('shaking');
                }
            }
        }, 5000);

        iconNotifications.addEventListener('show.bs.dropdown', function () {
            bellShake.setAttribute('data-unread-notifications', false);
            clearInterval(shakingInterval);
            bellShake.classList.remove('shaking');
            unreadNotifications.style.display = 'none';
        });
    }

    [].slice.call(d.querySelectorAll('[data-background]')).map(function (el) {
        el.style.background = 'url(' + el.getAttribute('data-background') + ')';
    });

    [].slice.call(d.querySelectorAll('[data-background-lg]')).map(function (el) {
        if (document.body.clientWidth > breakpoints.lg) {
            el.style.background = 'url(' + el.getAttribute('data-background-lg') + ')';
        }
    });

    [].slice.call(d.querySelectorAll('[data-background-color]')).map(function (el) {
        el.style.background = 'url(' + el.getAttribute('data-background-color') + ')';
    });

    [].slice.call(d.querySelectorAll('[data-color]')).map(function (el) {
        el.style.color = 'url(' + el.getAttribute('data-color') + ')';
    });

    // Tooltips
    var tooltipTriggerList = [].slice.call(d.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

    // Popovers
    var popoverTriggerList = [].slice.call(d.querySelectorAll('[data-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    })

    var scroll = new SmoothScroll('a[href*="#"]', {
        speed: 500,
        speedAsDuration: true
    });

    if (d.querySelector('.current-year')) {
        d.querySelector('.current-year').textContent = new Date().getFullYear();
    }
});


const humanFileSize = function (bytes, si = true, dp = 1) {
    const thresh = si ? 1000 : 1024;
    if (Math.abs(bytes) < thresh) {
        return bytes + ' B';
    }

    const units = si
        ? ['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
        : ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];
    let u = -1;
    const r = 10 ** dp;

    do {
        bytes /= thresh;
        ++u;
    } while (Math.round(Math.abs(bytes) * r) / r >= thresh && u < units.length - 1);

    return bytes.toFixed(dp) + ' ' + units[u];
}

const defaultDateTimeFormat = "YYYY-MM-DD HH:mm:ss";
const defaultDateFormat = "YYYY-MM-DD HH:mm:ss";

const handleSwalAxiosError = function (err) {
    let res = err.response;
    if (res && res.status === 400) {
        let message = '<span class="text-left">';
        for (const key in res.data) {
            message += `${key}: ${res.data[key]}`;
        }
        message += '</span>';
        Swal.showValidationMessage(message);
    } else {
        Swal.showValidationMessage(`Request failed: ${err}`);
    }
}
