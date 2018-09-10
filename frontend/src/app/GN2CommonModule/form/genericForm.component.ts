import {
  Component,
  OnInit,
  Input,
  Output,
  EventEmitter,
  AfterViewInit,
  OnDestroy
} from '@angular/core';
import { FormControl } from '@angular/forms';
import { Subscription } from 'rxjs/Subscription';

@Component({})
export class GenericFormComponent implements OnInit, AfterViewInit, OnDestroy {
  @Input() parentFormControl: FormControl;
  @Input() label: string;
  @Input() disabled: false;
  @Input() debounceTime: number;
  @Input() multiSelect: false;
  @Input() searchBar: false;
  @Input() displayAll: false; // param to display the field 'all' in the list, default at false
  @Output() onChange = new EventEmitter<any>();
  @Output() onDelete = new EventEmitter<any>();
  public sub: Subscription;

  constructor() {}

  ngOnInit() {
    this.debounceTime = this.debounceTime || 0;
  }

  ngAfterViewInit() {
    this.sub = this.parentFormControl.valueChanges
      .distinctUntilChanged()
      .debounceTime(this.debounceTime)
      .subscribe(value => {
        if (!value || (value && (value.length === 0 || value === ''))) {
          this.onDelete.emit();
        } else {
          this.onChange.emit(value);
        }
      });
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }
}
