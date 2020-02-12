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
    this.api.addTodo(todo);
    this.getTodos();
  }

  getTodos(): Todo[] {
    const result: Todo[] = this.api.getTodos();
    result.forEach((todo: Todo) => {
      this.todoSubject.next(todo);
    });
    this.todos = result;
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
