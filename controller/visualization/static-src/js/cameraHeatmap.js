"use strict";

import $ from "jquery";
import "bootstrap";
import flatpickr from "flatpickr";
import * as d3 from 'd3';
import * as d3Legend from 'd3-svg-legend';

const DATA_OPACITY = 0.3;
const CAMERA_IMAGE_MAP = {
    "1f-1": "/static/img/camera-1f-1.jpg",
    "1f-2": "/static/img/camera-1f-2.jpg",
    "2f-1": "/static/img/camera-2f-1.jpg",
}

class Heatmap {
    constructor() {
        let $svg = $("svg#chart-camera");
        this.chartWidth = $svg.width();
        this.chartHeight = $svg.height();
        this.tooltip = d3.select("body").append("div").attr("class", "tooltip").style("opacity", 0);
        this.chartArea = d3.select("svg#chart-camera");
        this.legendArea = d3.select("svg#legend-camera");
        this.bearer = $("input#bearer").val();
        this.path = $("input#path").val();
        this.cameraId = "";
        this.stVal = "";
        this.etVal = "";
        this.row = 0;
        this.column = 0;
    }

    show() {
        console.log("Heatmap#show(), cameraId=" + this.cameraId);

        $.ajax({
            type: "GET",
            url: this.path,
            headers: {
                Authorization: "Bearer " + this.bearer
            },
            data: {
                camera: this.cameraId,
                st: formatISO8601(new Date(this.stVal)),
                et: formatISO8601(new Date(this.etVal)),
            },
            dataType: "json"
        }).then((data, status, xhr) => {
            this.row = data.row;
            this.column = data.column;
            this.clear();
            this.plot(data.dataset)
        }).catch((xhr, status, e) => {
            console.error("error", xhr, ":", status, ":", e);
        });
    }

    plot(dataset) {
        console.log("Heatmap#plot()");

        let maxValue=d3.max(dataset);
        let colorScale = d3.scaleSequential(d3.interpolate("white", "red")).domain([0, maxValue]);

        this.chartArea.selectAll("rect")
                      .data(dataset)
                      .enter()
                      .append("rect")
                      .attr("class", "block")
                      .attr("x", (d, i) => (i % this.column) * this.chartWidth / this.column)
                      .attr("y", (d, i) => Math.floor(i / this.column) * this.chartHeight / this.row)
                      .attr("width", (d, i) => this.chartWidth / this.column)
                      .attr("height", (d, i) => this.chartHeight / this.row)
                      .style("fill", (d, i) => colorScale(d))
                      .style("opacity", DATA_OPACITY)
                      .on("mouseover", (d) => {
                          this.tooltip.transition().duration(500).style("opacity", 0);
                          this.tooltip.transition().duration(200).style("opacity", 0.7);
                          this.tooltip.transition().delay(1000).duration(200).style("opacity", 0);
                          this.tooltip.html("<b>" + d + "</b>")
                                      .style("left", d3.event.pageX + "px")
                                      .style("top", d3.event.pageY + "px");
                      });
        this.legendArea.append("g")
                       .attr("class", "legendSequential")
                       .attr("transform", "translate(20,20)");
        let legend = d3Legend.legendColor()
            .shapeWidth(30)
            .labelFormat(d3.format(".0f"))
            .scale(colorScale);
        this.legendArea.select(".legendSequential").call(legend);

        d3.selectAll("svg#legend-camera rect").each((d, i, nodes) => {
            d3.select(nodes[i]).style("opacity", DATA_OPACITY);
        });
    }

    clear() {
        console.log("Heatmap#clear()");

        this.chartArea.selectAll("rect").data([]).exit().remove();
        this.legendArea.selectAll("g").data([]).exit().remove();
    }
}

const formatISO8601 = (date) => {
    let o = date.getTimezoneOffset() / -60;
    let offset = ((0 < o) ? "+" : "-") + ("00" + Math.abs(o)).substr(-2) + ":00";

    return [
        [
            date.getFullYear(),
            ("00" + (date.getMonth() + 1)).substr(-2),
            ("00" + date.getDate()).substr(-2)
        ].join("-"),
        "T",
        [
            ("00" + date.getHours()).substr(-2),
            ("00" + date.getMinutes()).substr(-2),
            ("00" + date.getSeconds()).substr(-2)
        ].join(":"),
        offset
    ].join("");
};

const initFlatPickr = (heatmap) => {
    let $stDatetime = $("input#st_datetime_value");
    let $etDatetime = $("input#et_datetime_value");
    let $showButton = $("button#show_button");

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

    let onChangeDatetime = (event) => {
        heatmap.stVal = $stDatetime.val();
        heatmap.etVal = $etDatetime.val();

        if (heatmap.stVal && heatmap.etVal) {
            $showButton.prop("disabled", false);
        } else {
            $showButton.prop("disabled", true);
        }
    };
    $stDatetime.on("change", onChangeDatetime);
    $etDatetime.on("change", onChangeDatetime);
};

const initCameraSelector = (heatmap) => {
    let $camera = $("select#camera_id");
    let $image = $("div.chart-parent img.chart");
    heatmap.cameraId = $camera.val();

    $("select#camera_id").on("change", (event) => {
        heatmap.cameraId = $camera.val();
        heatmap.clear();
        $image.attr("src", CAMERA_IMAGE_MAP[heatmap.cameraId]);
    });
}

const initButton = (heatmap) => {
    let $stDatetime = $("input#st_datetime_value");
    let $etDatetime = $("input#et_datetime_value");
    let $showButton = $("button#show_button");
    let $clearButton = $("button#clear_button");

    $showButton.on("click", (event) => heatmap.show());
    $clearButton.on("click", (event) => {
        heatmap.clear();
        $stDatetime.val("");
        $etDatetime.val("");
        $showButton.prop("disabled", true);
    });
}

$(() => {
    let heatmap = new Heatmap();

    initFlatPickr(heatmap);
    initCameraSelector(heatmap);
    initButton(heatmap);
});
