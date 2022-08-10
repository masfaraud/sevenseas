import { Component, OnInit } from '@angular/core';

import Map from 'ol/Map';
import TileState from 'ol/TileState';
// import OSM from 'ol/source/OSM';
// import TileLayer from 'ol/layer/Tile';
import View from 'ol/View';
import WMTS from 'ol/source/WMTS';
import WMTSTileGrid from 'ol/tilegrid/WMTS';
import {get as getProjection} from 'ol/proj';
import {getTopLeft, getWidth} from 'ol/extent';

import Draw from 'ol/interaction/Draw';
import Overlay from 'ol/Overlay';
import {Circle as CircleStyle, Fill, Stroke, Style} from 'ol/style';
import {LineString, Polygon} from 'ol/geom';
import {OSM, Vector as VectorSource} from 'ol/source';
import {Tile as TileLayer, Vector as VectorLayer} from 'ol/layer';
import {getArea, getLength} from 'ol/sphere';
import {unByKey} from 'ol/Observable';


@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements OnInit {
  map: Map;

  constructor(
  ) { }

  ngOnInit(): void {
    this.create_map();
  }

  create_map(){

    const projection = getProjection('EPSG:3857');
    const projectionExtent = projection.getExtent();
    const size = getWidth(projectionExtent) / 256;
    const resolutions = new Array(19);
    const matrixIds = new Array(19);
    for (let z = 0; z < 19; ++z) {
      // generate resolutions and matrixIds arrays for this WMTS
      resolutions[z] = size / Math.pow(2, z);
      matrixIds[z] = z;
    }
    

    var wmts = new WMTS({
      attributions:
        '',
      url: 'http://localhost:5000/wmts/shom',
      layer: 'RASTER_MARINE_3857_WMTS',
      matrixSet: '3857',
      format: 'image/png',
      projection: projection,
      // Referer: "https://data.shom.fr/",
      tileGrid: new WMTSTileGrid({
        origin: getTopLeft(projectionExtent),
        resolutions: resolutions,
        matrixIds: matrixIds,
      }),
      style: 'normal',
      wrapX: true,
    })

    this.map = new Map({
      layers: [
        new TileLayer({
          // opacity: 0.3,
          minZoom: 12,
          source: new OSM()}),
        new TileLayer({
          // opacity: 1,
          source: wmts,
          maxZoom: 8,
        })
      ],
      target: 'map',
      view: new View({
        center: [-100000, 6000000],
        zoom: 4,
      }),
    });
  }

}
