<?xml version='1.0' encoding='UTF-8'?>
<Project Name="Template - Generic.lvproj" Type="Project" LVVersion="13008000" URL="/&lt;instrlib&gt;/_Template - Generic/Template - Generic.lvproj">
	<Property Name="Instrument Driver" Type="Str">True</Property>
	<Property Name="NI.Project.Description" Type="Str">This project is used by developers to edit API and example files for LabVIEW Plug and Play instrument drivers.</Property>
	<Item Name="My Computer" Type="My Computer">
		<Property Name="CCSymbols" Type="Str">OS,Win;CPU,x86;</Property>
		<Property Name="NI.SortType" Type="Int">3</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="Examples" Type="Folder">
			<Item Name="SC10 example.vi" Type="VI" URL="/&lt;instrlib&gt;/Thorlabs_SC10/Examples/SC10 example.vi"/>
		</Item>
		<Item Name="Data" Type="Folder">
			<Item Name="SC10CommandLib_win32.dll" Type="Document" URL="/&lt;instrlib&gt;/Thorlabs_SC10/Data/SC10CommandLib_win32.dll"/>
			<Item Name="SC10CommandLib_x64.dll" Type="Document" URL="/&lt;instrlib&gt;/Thorlabs_SC10/Data/SC10CommandLib_x64.dll"/>
		</Item>
		<Item Name="Thorlabs_SC10.lvlib" Type="Library" URL="/&lt;instrlib&gt;/Thorlabs_SC10/Thorlabs_SC10.lvlib"/>
		<Item Name="Dependencies" Type="Dependencies"/>
		<Item Name="Build Specifications" Type="Build">
			<Item Name="My Zip File" Type="Zip File">
				<Property Name="Absolute[0]" Type="Bool">false</Property>
				<Property Name="BuildName" Type="Str">My Zip File</Property>
				<Property Name="Comments" Type="Str"></Property>
				<Property Name="DestinationID[0]" Type="Str">{9546B992-EF07-4E2F-9089-DF1535D63B42}</Property>
				<Property Name="DestinationItemCount" Type="Int">1</Property>
				<Property Name="DestinationName[0]" Type="Str">Destination Directory</Property>
				<Property Name="IncludedItemCount" Type="Int">1</Property>
				<Property Name="IncludedItems[0]" Type="Ref">/My Computer</Property>
				<Property Name="IncludeProject" Type="Bool">true</Property>
				<Property Name="Path[0]" Type="Path">../../../../../../SharedFolder/build/SC10 LabVIEW Instrument Driver.zip</Property>
				<Property Name="ZipBase" Type="Str">NI_zipbasedefault</Property>
			</Item>
		</Item>
	</Item>
</Project>
