import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Routes, RouterModule } from '@angular/router';
import { GN2CommonModule } from '@geonature_common/GN2Common.module';
import { SyntheseComponent } from './synthese.component';
import { SyntheseListComponent } from './synthese-results/synthese-list/synthese-list.component';
import { SyntheseCarteComponent } from './synthese-results/synthese-carte/synthese-carte.component';
import { SyntheseSearchComponent } from './synthese-search/synthese-search.component';
import { DataService } from './services/data.service';
import { SyntheseFormService } from './services/form.service';
import { MapService } from '@geonature_common/map/map.service';
import { TreeModule } from 'angular-tree-component';
import { TaxonTreeModalComponent } from './synthese-search/taxon-tree/taxon-tree.component';

const routes: Routes = [{ path: '', component: SyntheseComponent }];

@NgModule({
  imports: [RouterModule.forChild(routes), GN2CommonModule, CommonModule, TreeModule.forRoot()],
  declarations: [
    SyntheseComponent,
    SyntheseListComponent,
    SyntheseCarteComponent,
    SyntheseSearchComponent,
    TaxonTreeModalComponent
  ],
  entryComponents: [TaxonTreeModalComponent],
  providers: [DataService, SyntheseFormService, MapService]
})
export class SyntheseModule {}
