import { Injectable } from '@angular/core';
import { Todo } from 'src/interfaces/todo';
import { of, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TodoService {

  private todos: Todo[] = [];
  private finished_todos: Todo[] = [];

  constructor() { }

  addTodo(todoTitle: string, dueDate?: Date) {
    this.todos.push({
      title: todoTitle,
      due_date: dueDate
    });
  }

  getTodos(): Todo[] {
    return this.todos;
  }

  todoSub(): Observable<Todo[]> {
    return of<Todo[]>(this.todos);
  }
}
