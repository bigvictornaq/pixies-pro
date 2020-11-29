var btn1 = $('#btnMostrar');

  $(document).ready( function () {
   //tabla con mayores
    $('#tbl_g').DataTable({
      dom:"rti"
    });
    //tabla con los valores menores
    $('#tbl_s').DataTable();
    //tabla con los valores moda
    $('#tbl_m').DataTable();
    //tabla dde MS-SQL
    $('#dataframe').DataTable({
    processing:true,
    ajax:"{{url_for('showdd')}}",
    columns:[
            { "data": "ID" },
            { "data": "firstName" },
            { "data": "email" },
            { "data": "address" },
            { "data": "zip" },
            { "data": "phone" },
            { "data": "ciudad" },
            { "data": "country" }

    ],
    dom:'Bfrtilp',
    buttons:[

    {
                "extend":'pdfHtml5',
                "text":'<i class="fas fa-file-pdf">&nbsp;PDF</i>',
                "titleAttr":'Exportar a PDF',
                "className":'btn btn-outline-danger'
            },
            

            {
                "extend":'excel',
                "text":'<i class="far fa-file-excel">&nbsp;Excel</i>',
                "titleAttr":'excel',
                "className":'btn-outline-success'
            },
    ]
  });

    var table = $('#tbl_ad').DataTable({
      processing:true,
      responsive:true,
    ajax:"{{url_for('dMsql')}}",
    columns:[
            { "data": "ID" },
            { "data": "firstName" },
            { "data": "email" },
            { "data": "address" },
            { "data": "zip" },
            { "data": "phone" },
            { "data": "ciudad" },
            { "data": "country" }

    ],
    dom:'Bfrtilp',
    buttons:[

    {
                "extend":'pdfHtml5',
                "text":'<i class="fas fa-file-pdf">&nbsp;PDF</i>',
                "titleAttr":'Exportar a PDF',
                "className":'btn btn-outline-danger'
            },
            {
                "extend":'print',
                "text":'<i class="fas fa-print">&nbsp;Print</i>',
                "titleAttr":'Print',
                "className":'btn btn-outline-info'
            },
            {
                "extend":'excel',
                "text":'<i class="far fa-file-excel">&nbsp;Excel</i>',
                "titleAttr":'excel',
                "className":'btn-outline-success'
            },

    ]
  });
  //tabla Posgresal
  var table2 = $('#tbl_dvd').DataTable({
    processing:true,
    responsive:true,
    ajax:"{{url_for('dpos')}}",
    columns:[
            { "data": "ID" },
            { "data": "firstName" },
            { "data": "email" },
            { "data": "address" },
            { "data": "zip" },
            { "data": "phone" },
            { "data": "ciudad" },
            { "data": "country" }

    ],
    dom:'Bfrtilp',
    buttons:[

    {
                "extend":'pdfHtml5',
                "text":'<i class="fas fa-file-pdf">&nbsp;PDF</i>',
                "titleAttr":'Exportar a PDF',
                "className":'btn btn-outline-danger'
            },
            {
                "extend":'print',
                "text":'<i class="fas fa-print">&nbsp;Print</i>',
                "titleAttr":'Print',
                "className":'btn btn-outline-info'
            },
            {
                "extend":'excel',
                "text":'<i class="far fa-file-excel">&nbsp;Excel</i>',
                "titleAttr":'excel',
                "className":'btn-outline-success'
            },
    ]
  });
//boton que muestra la informacion de la fase 2
btn1.on("click", function(){

  var datito;
  //Obtner los datos agrupados
  $.getJSON("{{url_for('paisG')}}",function(data){
    var salve =null;
    var codeName = {};
    var ncode;
    var ncame;
    var cnts ={}
    var continentsByGruoup ={}
//datos por continent?
$.ajax(
{
    url: "{{url_for('continentss')}}",
    dataType: "json",
    async: false,
    success: function(data)
    {
      var continente = data.map(function(s){
        return s.continent;
      });
      var pais = data.map(function(s){
        return s.country;
      })
     
     for (let i = 0; i < continente.length; i++) {
          cnts[pais[i]] = continente[i]; 
     }

    }
});
    //Obtner los datos con code EU necesarios par mapa
 $.ajax(
{
    url: "{{url_for('codeguito')}}",
    dataType: "json",
    async: false,
    success: function(data)
    {
      salve = data;
    }
});
//obtner los datos por pais code?
$.ajax(
{
    url: "{{url_for('codegui')}}",
    dataType: "json",
    async: false,
    success: function(data)
    {
      ncode = data.map(function(d){
        return d.Code
      });
      ncame = data.map(function(d){
        return d.Name
      });
      
      for(var j=0; j <ncode.length;j++){
        codeName[ncame[j]] =ncode[j]; 
      }
    }
}); 

function cats(datito){

    if(datito === "Kazakstan"){
      var menso = "Kazakhstan"
      return menso;
    }else if(datito == "Congo, The Democratic Republic of the"){
      var menso = "The Democratic Republic of Congo";
      return menso;
    }else{
      return datito;
    }

}
var piss;
var nCliente;
var objs = {};
//objeto de pruebas
var abs = {}
var noodle;
//obtner los datos del json en separados
piss = data.data.map(function(d){
  return d.Pais
});

nCliente = data.data.map(function(d){
  return d.NumeroClientes
});
//los datos obtneidos convertidos en objeto para su manupulacion
for(var i=0;i< piss.length;i++){
    objs[piss[i]] = nCliente[i];
}

//pruebas
for(var i=0;i<piss.length;i++){
   
    var sorete = codeName[piss[i]]
    abs[sorete] = nCliente[i] 
}
//obtner la lista de pais por continentes continentsByGruoup
var nelson;
var asia = 0;
for (let k = 0; k < piss.length; k++) {
      var soledads = cats(piss[k])
      var coconout = cnts[soledads]

      if( coconout === "Asia"){

        asia  = (nCliente[k] * 100) / 19107;
      }
        
      
}
console.log(asia)

//var valores = jvm.values.apply({},jvm.values(objs))
$('#world-map').vectorMap({
map: 'world_mill',
series: {
  regions: [{
    values:abs,
    scale:  ['#FEE5D9', '#A50F15'],
    normalizeFunction: 'polynomial',
    legend:{
      vertical:true
    }
  }]
},
onRegionTipShow: function(e, el, code){
    noodle = salve[code]
    el.html(el.html()+' Numero de clientes - '+abs[code]+')');
  }

});

  });
  
  mostrarDatos();
  $('#informacion').show();
  

});

  });//final

function mostrarDatos() {
  //Tabla de analisis con los datos unidos

  var table4 = $('#tbl_paiss').DataTable({
    processing:true,
    responsive:true,
    ajax:"{{url_for('paisG')}}",
    columns:[
            { "data": "Pais" },
            { "data": "NumeroClientes" }
    ],
    dom:'Bfrtilp',
    buttons:[

    {
                "extend":'pdfHtml5',
                "text":'<i class="fas fa-file-pdf">&nbsp;PDF</i>',
                "titleAttr":'Exportar a PDF',
                "className":'btn btn-outline-danger'
            },
            {
                "extend":'excel',
                "text":'<i class="far fa-file-excel">&nbsp;Excel</i>',
                "titleAttr":'excel',
                "className":'btn-outline-success'
            },
    ]
  });

  

}