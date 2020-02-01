import { Injectable } from '@angular/core';
import { Todo } from 'src/interfaces/todo';
import { from, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TodoService {

  private todos: Todo[] = [];
  private todoSubject: Subject<Todo> = new Subject<Todo>();
  private index = 0;

  constructor() { }

  addTodo(todoTitle: string, dueDate?: Date) {
    const todo: Todo = {title: todoTitle, due_date: dueDate, finished: false, id: this.index++};
    this.todos.push(todo);
    this.todoSubject.next(todo);
  }

  getTodos(): Todo[] {
    return this.todos;
  }

  todoSub() {
    return this.todoSubject;
  }

  finishTodo(id: number) {
    const finishedTodo = this.todos[id];
    console.log(finishedTodo);
    finishedTodo.finished = true;
    this.todoSubject.next(finishedTodo);
  }
}
