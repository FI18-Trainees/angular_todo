import { Component, OnInit, OnDestroy } from '@angular/core';
import { Observable, Subscription, Observer } from 'rxjs';
import { Todo } from 'src/interfaces/todo';
import { TodoService } from 'src/services/todo.service';
import { MatCheckboxChange } from '@angular/material';
import { SidenavService } from 'src/services/sidenav.service';

@Component({
  selector: 'app-list-view',
  templateUrl: './list-view.component.html',
  styleUrls: ['./list-view.component.scss']
})
export class ListViewComponent implements OnInit, OnDestroy {

  openTodos: Todo[] = [];
  finishedTodos: Todo[] = [];
  private todoSubscription: Subscription;

  constructor(private todoService: TodoService, private sidenavService: SidenavService) {
    this.todoSubscription = this.todoService.todoSub().subscribe((todo: Todo) => {
        if (todo.finished) {
          const index: number = this.openTodos.indexOf(todo);
          if (index !== -1) {
            this.openTodos.splice(index, 1);
          }
          this.finishedTodos.push(todo);
        } else {
          const index: number = this.finishedTodos.indexOf(todo);
          if (index !== -1) {
            this.finishedTodos.splice(index, 1);
          }
          this.openTodos.push(todo);
        }
    });
  }

  ngOnInit() {
    // filter for todos with finished = false
  }

  ngOnDestroy(): void {
    this.todoSubscription.unsubscribe();
  }

  todoFinished(id: number) {
    this.todoService.finishTodo(id);
  }

  showOpenTodoDetails(id: number) {
    this.sidenavService.open(this.openTodos[id]);
  }

  showFinishedTodoDetails(id: number) {
    this.sidenavService.open(this.finishedTodos[id]);
  }
}
