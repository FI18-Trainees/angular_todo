import { Injectable } from '@angular/core';
import { Todo } from 'src/interfaces/todo';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  addTodo(todo: Todo) {
    this.http.post('/api/todo', JSON.stringify(todo));
  }

  getTodos(): Todo[] {
    return null;
  }
}
