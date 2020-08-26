import { Component, OnInit, OnDestroy, Input } from "@angular/core";
import { filter, map, first } from "rxjs/operators";
import { leafletDrawOption } from "@geonature_common/map/leaflet-draw.options";
import { CommonService } from "@geonature_common/service/common.service";
import { ModuleConfig } from "../../module.config";
import { OcctaxFormMapService } from "./map.service";
import { OcctaxFormService } from "../occtax-form.service";

@Component({
  selector: "pnx-occtax-form-map",
  templateUrl: "map.component.html",
})
export class OcctaxFormMapComponent implements OnInit, OnDestroy {
  public leafletDrawOptions: any;
  public firstFileLayerMessage = true;
  public occtaxConfig = ModuleConfig;

  public coordinates = null;
  public geometry = null;
  public firstGeom = true;

  constructor(
    private ms: OcctaxFormMapService,
    private _commonService: CommonService,
    private _occtaxFormService: OcctaxFormService
  ) { }

  ngOnInit() {
    // overight the leaflet draw object to set options
    // examples: enable circle =>  leafletDrawOption.draw.circle = true;
    leafletDrawOption.draw.circle = false;
    leafletDrawOption.draw.rectangle = false;
    leafletDrawOption.draw.marker = false;
    leafletDrawOption.draw.polyline = true;
    leafletDrawOption.edit.remove = false;
    this.leafletDrawOptions = leafletDrawOption;
    // set the input for the marker component
    // set the coord only when load data and when its edition mode (id_releve)
    // after the marker component does it by itself whith the ouput
    // when modifie the coordinates innput, it create twice the marker
    this.ms.geojson
      .pipe(
        filter(
          (geojson) =>
            geojson !== null &&
            this._occtaxFormService.id_releve_occtax.getValue() !== null
        ),
        map((geojson) => geojson.geometry),
        first()
      )
      .subscribe((geometry) => {
        if (geometry.type == "Point") {
          this.coordinates = geometry.coordinates;
        } else {
          // set the input for leafletdraw component
          this.geometry = geometry;
        }
      });
  }

  // display help toaster for filelayer
  infoMessageFileLayer() {
    if (this.firstFileLayerMessage) {
      this._commonService.translateToaster("info", "Map.FileLayerInfoMessage");
    }
    this.firstFileLayerMessage = false;
  }

  sendGeoInfo(geojson) {
    this.ms.geometry = geojson;
  }

  ngOnDestroy() {
    this.ms.reset();
  }
}
