import { Injectable } from '@angular/core';
import { Todo } from 'src/interfaces/todo';
import { Subject, Observable } from 'rxjs';
import { Priority } from 'src/enums/priority.enum';
import { ApiService } from './api.service';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class TodoService {

  private todos: Todo[] = [];
  private todoSubject: Subject<Todo> = new Subject<Todo>();
  private index = 0;

  constructor(private api: ApiService, private http: HttpClient) { }

  addTodo(todoTitle: string, dueDate?: Date) {
    const todo: Todo = {title: todoTitle, due_date: dueDate, finished: false, id: this.index++, list: 'default', priority: Priority.normal};
    todo.id = this.api.addTodo(todo);
    this.todoSubject.next(todo);
    this.getTodos();
  }

  getTodos(): Observable<Todo[]> {

    return this.api.getTodos().pipe(
      map((todos: Todo[]) => {
        this.todos = todos;
        return todos;
      })
    );
  }

  initialize() {
    this.getTodos().subscribe((todos: Todo[]) => {
      todos.forEach((todo: Todo) => {
        this.todoSubject.next(todo);
      });
    });
  }

  todoSub() {
    return this.todoSubject;
  }

  finishTodo(id: number) {
    const finishedTodo = this.todos[id];
    finishedTodo.finished = !finishedTodo.finished;
    this.todos[id] = finishedTodo;
    this.getTodos();
    // this.api.updateTodo(finishedTodo);
  }
}
