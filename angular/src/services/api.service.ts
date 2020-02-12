import { Injectable } from '@angular/core';
import { Todo } from 'src/interfaces/todo';
import { HttpClient } from '@angular/common/http';
import { from } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class ApiService {

  url = '/api/todo';

  constructor(private http: HttpClient) { }

  addTodo(todo: Todo) {
    this.http.post(this.url, JSON.stringify(todo)).subscribe(data => console.log(data));
  }

  getTodos(): Todo[] {
    let result: Todo[] = [];
    return result;
  }
}
