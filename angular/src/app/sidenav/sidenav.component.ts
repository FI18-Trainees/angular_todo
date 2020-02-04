import { Component, OnInit, ViewChild } from '@angular/core';
import { Todo } from 'src/interfaces/todo';
import { SidenavService } from 'src/services/sidenav.service';

@Component({
  selector: 'app-sidenav',
  templateUrl: './sidenav.component.html',
  styleUrls: ['./sidenav.component.scss']
})
export class SidenavComponent implements OnInit {

  displayedTodo: Todo;

  constructor(private sidenavService: SidenavService) { }

  ngOnInit() {
    this.sidenavService.todoSub().subscribe((todo: Todo) => {
      this.displayedTodo = todo;
    });
  }
}
