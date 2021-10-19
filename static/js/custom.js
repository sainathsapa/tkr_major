
	$('table').DataTable();
	
	
    function openNav() {
      document.getElementById("mySidenav").style.width = "250px";
      document.getElementById("main").style.marginLeft = "250px";
          document.getElementById("cbtn").style.display = "inline-block";
         document.getElementById("obtn").style.display = "none";
    }
    
    function closeNav() {
      document.getElementById("mySidenav").style.width = "0";
      document.getElementById("main").style.marginLeft= "0";
              document.getElementById("obtn").style.display = "inline-block";
         document.getElementById("cbtn").style.display = "none";
    }
    
               new WOW().init();
          
    $(document).ready(function() {
        $('#example').DataTable( {
            dom: 'Bfrtip',
            buttons: [
                'copy', 'csv', 'excel', 'pdf', 'print'
            ]
        } );
    } );
              