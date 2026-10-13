# Exporta los juegos de tu copia de GameBase64 (GBC_v19.mdb) a un CSV
# que usa build_catalog.py. Requiere el driver ODBC de Microsoft Access (64 bits).
#
# Uso:  powershell -File export_gb64.ps1 -Mdb "C:\ruta\GBC_v19.mdb" -Out games.csv
param(
  [Parameter(Mandatory=$true)][string]$Mdb,
  [string]$Out = "games.csv"
)
$ErrorActionPreference = 'Stop'
try {
$cn = New-Object System.Data.Odbc.OdbcConnection("Driver={Microsoft Access Driver (*.mdb, *.accdb)};Dbq=$Mdb;")
$cn.Open()
$cmd = $cn.CreateCommand()
$cmd.CommandText = "SELECT g.GA_Id, g.Name, y.[Year], p.Publisher, ge.Genre, pg.ParentGenre, g.Rating, g.ScrnshotFilename, g.CloneOf " +
  "FROM ((((Games g LEFT JOIN Years y ON g.YE_Id=y.YE_Id) LEFT JOIN Publishers p ON g.PU_Id=p.PU_Id) " +
  "LEFT JOIN Genres ge ON g.GE_Id=ge.GE_Id) LEFT JOIN PGenres pg ON ge.PG_Id=pg.PG_Id)"
$da = New-Object System.Data.Odbc.OdbcDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
[void]$da.Fill($dt)
$cn.Close()
$da.Dispose(); $cmd.Dispose(); $cn.Dispose()
[System.Data.Odbc.OdbcConnection]::ReleaseObjectPool()
$dt | Export-Csv -NoTypeInformation -Encoding UTF8 $Out
"Exportados $($dt.Rows.Count) juegos a $Out"
} catch {
  Write-Error "No se pudo exportar / Export failed: $_  (falta el driver ODBC de Access? / Access ODBC driver missing?)"
  exit 1
}
exit 0
