"use strict";

import $ from "jquery";
import "bootstrap";
import flatpickr from "flatpickr";


class Heatmap {
    show() {
        console.log("Heatmap#show()");
        const bearer = $("input#bearer").val();
        const path = $("input#path").val();

        let stVal = $("input#st_datetime_value").val();
        let etVal = $("input#et_datetime_value").val();

        $.ajax({
            type: "GET",
            url: path,
            headers: {
                Authorization: "Bearer " + bearer
            },
            data: {
                st: formatISO8601(new Date(stVal)),
                et: formatISO8601(new Date(etVal)),
            },
            dataType: "json"
        }).then((data, status, xhr) => {
            console.log("success", data, ":", status, ":", xhr);
        }).catch((xhr, status, e) => {
            console.error("error", xhr, ":", status, ":", e);
        });
    }
}

const formatISO8601 = (date) => {
    let o = date.getTimezoneOffset() / -60;
    let offset = ((0 < o) ? '+' : '-') + ('00' + Math.abs(o)).substr(-2) + ':00';

    return [
        [
            date.getFullYear(),
            ('00' + (date.getMonth() + 1)).substr(-2),
            ('00' + date.getDate()).substr(-2)
        ].join('-'),
        'T',
        [
            ('00' + date.getHours()).substr(-2),
            ('00' + date.getMinutes()).substr(-2),
            ('00' + date.getSeconds()).substr(-2)
        ].join(':'),
        offset
    ].join('');
};

const initFlatPickr = () => {
    let now = new Date();
    let options = {
        wrap: true,
        enableTime: true,
        enableSeconds: true,
        time_24hr: true,
        dateFormat: "Y-m-d H:i:S",
        defaultHour: now.getHours(),
        defaultMinute: now.getMinutes(),
    };
    flatpickr(".st_datetime", options);
    flatpickr(".et_datetime", options);

    let onChangeDatetime = () => {
        let stVal = $("input#st_datetime_value").val();
        let etVal = $("input#et_datetime_value").val();
        let $show_button = $("button#show_button");

        if (stVal && etVal) {
            $show_button.prop("disabled", false);
        } else {
            $show_button.prop("disabled", true);
        }
    };
    $("div.st_datetime input#st_datetime_value").on("change", onChangeDatetime);
    $("div.et_datetime input#et_datetime_value").on("change", onChangeDatetime);
};

$(() => {
    initFlatPickr();

    let heatmap = new Heatmap();
    $("button#show_button").on("click", event => heatmap.show());
});
