import { Injectable } from '@angular/core';
import { Todo } from 'src/interfaces/todo';
import { from, Subject } from 'rxjs';
import { Priority } from 'src/enums/priority.enum';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root'
})
export class TodoService {

  private todos: Todo[] = [];
  private todoSubject: Subject<Todo> = new Subject<Todo>();
  private index = 0;

  constructor(private api: ApiService) { }

  addTodo(todoTitle: string, dueDate?: Date) {
    const todo: Todo = {title: todoTitle, due_date: dueDate, finished: false, id: this.index++, list: 'default', priority: Priority.normal};
    this.todos.push(todo);
    this.todoSubject.next(todo);
    this.api.addTodo(todo);
  }

  getTodos(): Todo[] {
    return this.todos;
  }

  todoSub() {
    return this.todoSubject;
  }

  finishTodo(id: number) {
    const finishedTodo = this.todos[id];
    finishedTodo.finished = !finishedTodo.finished;
    this.todoSubject.next(finishedTodo);
  }
}
