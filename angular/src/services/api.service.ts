import { Injectable } from '@angular/core';
import { Todo } from 'src/interfaces/todo';
import { HttpClient } from '@angular/common/http';
import { IApiResponse } from 'src/interfaces/apiResponse';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  url = '/api/todo';

  addTodo(todo: Todo): number {
    let id = 0;
    this.http.post(this.url, JSON.stringify(todo)).subscribe((data: IApiResponse) => {
      id = data.todo_id;
    });
    return id;
  }

  getTodos(): Observable<Todo[]> {
    return this.http.get<Todo[]>(this.url);
  }

  updateTodo(todo: Todo) {
    let response: IApiResponse;
    this.http.post(this.url, todo.id + ':' + JSON.stringify(todo)).subscribe((data: IApiResponse) => {
      response = data;
    });
    if (response.status === 'success') {
      console.log('Updated');
    } else {
      console.error('Update failed due to reason:' + response.message);
    }
  }

}
