import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
import { Todo } from 'src/interfaces/todo';

@Injectable({
  providedIn: 'root'
})
export class SidenavService {

  private openSubject: Subject<boolean> = new Subject<boolean>();
  private todoSubject: Subject<Todo> = new Subject<Todo>();

  constructor() { }

  open(clickedTodo: Todo) {
    this.openSubject.next();
    this.todoSubject.next(clickedTodo);
  }

  sub(): Subject<boolean> {
    return this.openSubject;
  }

  todoSub(): Subject<Todo> {
    return this.todoSubject;
  }
}
