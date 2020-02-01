import { Component, OnInit, OnDestroy } from '@angular/core';
import { Observable, Subscription, Observer } from 'rxjs';
import { Todo } from 'src/interfaces/todo';
import { TodoService } from 'src/services/todo.service';
import { MatCheckboxChange } from '@angular/material';

@Component({
  selector: 'app-list-view',
  templateUrl: './list-view.component.html',
  styleUrls: ['./list-view.component.scss']
})
export class ListViewComponent implements OnInit, OnDestroy {

  openTodos: Todo[] = [];
  finishedTodos: Todo[] = [];
  private todoSubscription: Subscription;

  constructor(private todoService: TodoService) {
    this.todoSubscription = this.todoService.todoSub().subscribe((todo: Todo) => {
        if (!todo.finished) {
          this.openTodos.push(todo);
        } else {
          const index: number = this.openTodos.indexOf(todo);
          if (index !== -1) {
            this.openTodos.splice(index, 1);
          }
          this.finishedTodos.push(todo);
        }
    });
  }

  ngOnInit() {
    // filter for todos with finished = false
  }

  ngOnDestroy(): void {
    this.todoSubscription.unsubscribe();
  }

  todoFinished(evt: MatCheckboxChange) {
    if (evt.checked) {
      console.log(evt.source.id);
      this.todoService.finishTodo(+evt.source.id);
    }
  }
}
