import { Component, OnInit } from '@angular/core';
import { TodoService } from 'src/services/todo.service';
import { MatSnackBar, MatSnackBarConfig } from '@angular/material';

@Component({
  selector: 'app-input',
  templateUrl: './input.component.html',
  styleUrls: ['./input.component.scss']
})
export class InputComponent implements OnInit {

  inputValue = '';
  selectedDate: Date;
  private snackBarConfig: MatSnackBarConfig = { duration: 1500, panelClass: 'bg-red' };

  constructor(private todoService: TodoService, private errorSnackbar: MatSnackBar) {
  }

  ngOnInit() {
  }

  handleInput(e: KeyboardEvent) {
    e.preventDefault();
    if (this.inputValue.trim().length > 0) {
      if (this.selectedDate) {
        this.todoService.addTodo(this.inputValue, this.selectedDate);
        this.selectedDate = null;
      } else {
        this.todoService.addTodo(this.inputValue);
      }
      this.inputValue = '';
    } else {
      this.errorSnackbar.open('Enter a valid todo!', '', this.snackBarConfig);
    }
  }
}
