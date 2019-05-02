import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable }  from 'rxjs';
import { map }  from 'rxjs/operators';
import { AppConfig } from '../../../conf/app.config';
import { Role } from './form.service';

@Injectable()
export class UserDataService {
  constructor(private _http: HttpClient) {}

  getRole(id: number) {
    return this._http.get<any>(`${AppConfig.API_ENDPOINT}/users/role/${id}`);
  }

  getRoles(params?: any) {
    let queryString: HttpParams = new HttpParams();
    // tslint:disable-next-line:forin
    for (let key in params) {
      if (params[key] !== null) {
        queryString = queryString.set(key, params[key]);
      }
    }
    return this._http.get<any>(`${AppConfig.API_ENDPOINT}/users/roles`, { params: queryString });
  }

  put(role: Role): Observable<Role> {
    console.log("put");
    const options = JSON.stringify(role);
    return this._http
            .get<any>(`${AppConfig.API_ENDPOINT}/users/role_test`)
            .pipe(
                map((res: Role) => { 
                  return res;
                })
               );
  }

}
