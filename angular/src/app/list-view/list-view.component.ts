import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { Todo } from 'src/interfaces/todo';
import { TodoService } from 'src/services/todo.service';
import { SidenavService } from 'src/services/sidenav.service';

@Component({
  selector: 'app-list-view',
  templateUrl: './list-view.component.html',
  styleUrls: ['./list-view.component.scss'],
  providers: []
})
export class ListViewComponent implements OnInit, OnDestroy {

  openTodos: Todo[] = [];
  finishedTodos: Todo[] = [];
  private todoSubscription: Subscription;

  constructor(private todoService: TodoService, private sidenavService: SidenavService) {
  }

  ngOnInit() {
    this.todoSubscription = this.todoService.todoSub().subscribe((todo: Todo) => {
      if (todo.finished) {
        this.finishedTodos.push(todo);
      } else {
        this.openTodos.push(todo);
      }
    });
    this.todoService.initialize();
  }

  ngOnDestroy(): void {
    this.todoSubscription.unsubscribe();
  }

  todoFinished(id: number) {
    this.todoService.finishTodo(id);
  }

  showOpenTodoDetails(id: number) {
    this.sidenavService.open(this.openTodos.find(item => item.id === id));
  }

  showFinishedTodoDetails(id: number) {
    this.sidenavService.open(this.finishedTodos.find(item => item.id === id));
  }
}
