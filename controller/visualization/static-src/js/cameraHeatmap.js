'use strict';

import 'bootstrap';
import $ from 'jquery';

class Heatmap {
    show() {
        console.log("Heatmap#show()");
        const bearer = $("input#bearer").val();
        const path = $("input#path").val();

        $.ajax({
            type: "GET",
            url: path,
            headers: {
                'Authorization': 'Bearer ' + bearer
            },
            data: {
            },
            dataType: 'json'
        }).then((data, status, xhr) => {
            console.log("success", data, ":", status, ":", xhr);
        }).catch((xhr, status, e) => {
            console.error("error", xhr, ":", status, ":", e);
        });
    }
}

$(() => {
    let heatmap = new Heatmap();
    heatmap.show();
});
