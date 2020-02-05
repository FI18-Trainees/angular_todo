import { Component } from '@angular/core';
import { SidenavService } from 'src/services/sidenav.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'todo';

  opened = false;

  constructor(private sidenavService: SidenavService) {
    this.sidenavService.sub().subscribe(() => {
      this.opened = true;
    });
  }
}