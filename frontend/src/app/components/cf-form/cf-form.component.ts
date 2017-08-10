import { Component, OnInit } from '@angular/core';
import {FormControl} from '@angular/forms';
import 'rxjs/add/operator/startWith';
import 'rxjs/add/operator/map';

@Component({
  selector: 'app-cf-form',
  templateUrl: './cf-form.component.html',
  styleUrls: ['./cf-form.component.scss']
})
export class CfFormComponent implements OnInit {
  taxonomiques = [
    {value: 'Mammifères', viewValue: 'Mammifères'},
    {value: 'Oiseaux', viewValue: 'Oiseaux'},
    {value: 'Reptiles', viewValue: 'Reptiles'},
    {value: 'Amphibiens', viewValue: 'Amphibiens'},
    {value: 'Poissons', viewValue: 'Poissons'},
  ];
  stateCtrl: FormControl;
  filteredTaxons: any;
  taxons = [
    'Abacoproeces',
    'Abarenicola claparedi ',
    'Callizona nasuta Greeff',
    'Drassodex heeri ',
    'Eumeella',
    'Escargotin hérisson',
    'Epervier dEurope',
    'Dichagyris signifera',
    'Hieracium juraniforme Zahn',
    'Lathyrus linifolius (Reichard) Bässler',
    'Leuzea conifera (L.) DC.'
  ];
  constructor() {
    this.stateCtrl = new FormControl();
    this.filteredTaxons = this.stateCtrl.valueChanges
        .startWith(null)
        .map(name => this.filterTaxons(name));
  }

  ngOnInit() {
  }

  filterTaxons(val: string) {
    return val ? this.taxons.filter(s => s.toLowerCase().indexOf(val.toLowerCase()) === 0)
               : this.taxons;
  }

}
