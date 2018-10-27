"use strict";

import $ from "jquery";
import "bootstrap";
import flatpickr from "flatpickr";
import * as d3 from 'd3';
import * as d3Legend from 'd3-svg-legend';

const ROW = 9;
const COLUMN = 12;
const DATA_OPACITY = 0.3;
const CAMERA_IMAGE_MAP = {
    "1f-1": "/static/img/camera-1f-1.jpg",
    "1f-2": "/static/img/camera-1f-2.jpg",
    "2f-1": "/static/img/camera-2f-1.jpg",
}

class Heatmap {
    constructor() {
        this.cameraId = "";
    }

    show() {
        console.log("Heatmap#show(), cameraId=" + this.cameraId);
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

        let dataset = [];
        for (let i = 0; i < ROW; i++) {
            for (let j = 0; j < COLUMN; j++) {
                dataset.push(i + j);
            }
        }

        let $svg = $("svg#chart-camera");
        let w = $svg.width();
        let h = $svg.height();

        let tooltip = d3.select("body").append("div").attr("class", "tooltip").style("opacity", 0);

        let chart = d3.select("svg#chart-camera").selectAll("rect").data(dataset);
        let maxValue=d3.max(dataset);
        let colorScale = d3.scaleSequential(d3.interpolate("white", "red")).domain([0, maxValue]);
        chart.enter()
             .append("rect")
             .attr("class", "block")
             .attr("x", (d, i) => (i % COLUMN) * w / COLUMN)
             .attr("y", (d, i) => Math.floor(i / COLUMN) * h / ROW)
             .attr("width", (d, i) => w / COLUMN)
             .attr("height", (d, i) => h / ROW)
             .style("fill", (d, i) => colorScale(d))
             .style("opacity", DATA_OPACITY)
             .on("mouseover", (d) => {
                 tooltip.transition().duration(500).style("opacity", 0);
                 tooltip.transition().duration(200).style("opacity", 0.7);
                 tooltip.transition().delay(1000).duration(200).style("opacity", 0);
                 tooltip.html("<b>" + d + "</b>")
                        .style("left", d3.event.pageX + "px")
                        .style("top", d3.event.pageY + "px");
             });

        let legendArea = d3.select("svg#legend-camera");
        legendArea.append("g")
                  .attr("class", "legendSequential")
                  .attr("transform", "translate(20,20)");
        let legend = d3Legend.legendColor()
            .shapeWidth(30)
            .labelFormat(d3.format(".0f"))
            .scale(colorScale);
        legendArea.select(".legendSequential").call(legend);

        d3.selectAll("svg#legend-camera rect").each((d, i, nodes) => {
            d3.select(nodes[i]).style("opacity", DATA_OPACITY);
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

const initCameraSelector = (heatmap) => {
    let $camera = $("select#camera_id");
    let $image = $("div.chart-parent img.chart");
    heatmap.cameraId = $camera.val();

    $("select#camera_id").on("change", (event) => {
        heatmap.cameraId = $camera.val();
        $image.attr("src", CAMERA_IMAGE_MAP[heatmap.cameraId]);
    });
}

$(() => {
    let heatmap = new Heatmap();

    initFlatPickr();
    initCameraSelector(heatmap);

    $("button#show_button").on("click", event => heatmap.show());
});
