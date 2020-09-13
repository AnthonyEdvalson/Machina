# MACHINA

Machina is an advanced data aggregator that uses Python, Scylla, and Corvus to gather data over a distributed network.


# Overview

## Goals & Priorities

Goals:

1. Provide a framework that allows for retrieval and storage of large datasets
2. Process data to calculate any reasonable metric at incredible speeds for large data sets
3. Automatically gather or generate data on entities
4. Provide tools to find problematic areas of code, and bottlenecks
5. Provide tools to make writing fast code easier

Priorities (in order):

1. Speed
2. Extendibility / Modularity
3. Accuracy and Precision
4. Simplicity



## Uses

Machina can gather, store, and process large datasets on any entity, the intended use case is for tracking businesses and markets for investing. Here are some anitcipated use cases

| Entity                  | Sources                                                      |
| :---------------------- | :----------------------------------------------------------- |
| Businesses              | Patreon, [Websites], [Social Media], Google, Propublica, Wikipedia, [News], Yelp |
| Websites                | SimilarWeb, Quantcast, Alexa, Wikipedia                      |
| Songs                   | Spotify, Google Play                                         |
| Movies                  | OMBD, IMBD                                                   |
| Games                   | Steam Spy, App Store, Google Play                            |
| Video                   | YouTube, Twitch, Netflix                                     |
| Social&nbsp;Media&nbsp; | Reddit, Facebook, Twitter, Instagram                         |
| News                    | Google, Reddit, Facebook                                     |
| Trends                  | Google Trends                                                |

Square brackets are for entities that get data from other entities. For example, business data will be collected from APIs, one of these APIs is used to get website information from the current Machina system.

This “recursive” data is an important feature of Machina, it allows computed data to be shared between separate projects. This minimizes the amount of code needed, since data that is gathered for one purpose can be used elsewhere.



# Network Structure

The Machina network is all of the devices and programs that make up a single instance of Machina. This section describes the entire network at a high level, and describes the larger structures and design features that can be found in Machina.

## Vertex

Vertex is a management system that ties together all nodes in the system from various layers. This system is described in much more detail in the Vertex section

## Layers

Layers are an abstract structure of the application. Data flows from one layer to the next, becoming more refined in the process. There are 6 layers in Machina, each detailed in this document.

## Nodes

Node are the workers of Machina, they request tasks to collect, process, and store data.

## Data

Data is stored in Scylla, a nosql database based on Cassandra, but is much more optimized. The database is split into two databases. One is the “dump” database, the other is “clean”. 

Dump is a place where large volumes of raw information is stored temporarily. It may have many missing fields, and in general is not efficient to work with. It stores information from a particular query, along with the time stamp for when the data was collected.

Clean is where lightly processed data is put. Periodically, data from the dump is pulled, processed, and saved in the clean database. The main purpose of this process is to combine data from multiple sources.

When a row is added to the dump, the entire row has only come from a single query. By adding this intermediate step, it allows data from multiple sources coming in within a small window of time to be combined. This comes at a cost to responsiveness, as data is not immediately ready for use after storage.



# Global Utilities

 Global utilities are tools shared among multiple layers


## Events

Events provide a simple tool to implement a publish-subscribe system. An event is an object that can be subscribed to. When subscribing, a callback function must be passed in. This function will then be called when the event is invoked. This functionality is not built into Python, so it has been added here


## Socket Communication (com)

Socket communications are how all nodes communicate. It provides a uniform mode of communication that ties together the entire application. Because of this, it needs to be flexible and easy to send and receive information. Com provides various tools to help with this process

### SocketServer

SocketServer is a simple server that runs on sockets, it handles incoming threads in a callback function set at initialization.

### SocketClient

SocketClients are a convenient way to send data to a SocketServer. They handle parsing of information

### Alpha

Alpha is the internal application protocol used over the sockets, it has many similarities to HTTP:

```http
<4 byte length of message>
Path/For/Task
json
Header1: value
Header2: 5
Sender: name

{
    "data": [ "stored", "in", "here" ]
}
```

The main differences are the length at the start of the message, and the “path”. The length is not the length of the content, it is the length of the entire message (excluding the first 4 bytes). This makes parsing much easier, with a tiny hit to readability. The path is a description of what task needs to be done, and the format of the data.

#### Alpha Paths (APs)

Alpha paths are a way to uniquely identify resources in Machina, in the same way URLs uniquely identify resources on the web

### SmartServer

SmartServer is a class that uses a SocketServer, but in a much nicer way that is easier to work with. Here is how to set up a simple SmartServer:

```python
class ExampleServer(SmartServer):
    def __init__(self, host, port, name):
        super().__init__(host, port, name)
        
        self.add_routes([('Simple/Connect', self.connect),
                         ('Simple/Disconnect', self.disconnect)])
    
    def connect(req):
        # Process request
        return value
    
    def disconnect(req)
    	  # Do work
        return True
        
    
def main()
	  c = Config()
	  server = ExampleServer(c.get_str("host"),
                           c.get_int("port"),
                           c.get_str("name"))
    
    while True:
        server.serve()
        
main()
```

SmartServer will take care of nearly all the server details. In this case, running main will start a server on a host and port specified from a config. Then if a request is received on that port, the request will be parsed, if the path matches any of the @route decorators, that function will be run on its own thread. After that, the value that is returned is parsed and sent back as a response.

## Configuration Parsing

​Configuration parsing is used at all levels of the program and defines all constant parameters that are used during execution, as well as some source code. Configuration files are designed to be interchangeable, using a different config file for another project shouldn't cause any errors for missing code.

Configurations are stored in a folder with the extension, with a hierarchy with the following structure:

```
Config
- Default
  - protos
      Type\_1.proto
      ...
  - sources
      Source\_1.ini
      ...
  - aggregators
      Aggregator_1.ini
      ...
  - suppliers
      Supplier_1.ini
      ...
    Layer0.ini
    Layer1.ini
    ...
    Global.ini
- Dev
  ...
- Prod
  ...
```

​	However, this is not the same format that is used at runtime. The configuration has to be compiled first. Configuration compilation is needed because for several reasons

1. There may be additional source code in the config that need to be compiled
2. No layer needs all information in the config file, so ideally, we'd want a config for each layer only containing what it needs.
3. This allows all configuration data to be in one place for easy modification, and allows each layer to only get the files in the configuration that it cares about.
4. Configuration can be stored in its own repository, allowing for easier versioning and distribution

​	When building, a single .mach file is made for each layer, this file is a zipped version of the config file structure with unnecessary files removed, and source code compiled. The set of .mach files should then be uploaded to the config repository so that the nodes can receive the new configuration. 

​	Possibly the biggest benefit of this configuration system, is that it allows for multiple Machina networks for different purposes to run off the same code base. Because the only thing that changes their functionality is the config file, creating a second project only requires an additional config repository and config folder.

​	The Config Parser makes accessing this data straightforward, data can be requested with type and name. So Source\_2.ini data can be read with Config(&quot;Source&quot;, &quot;Source\_2&quot;).get(&quot;key&quot;). Data for a specific deployment mode (Dev / Prod) will override Default Values.



## Data Sharing

Python

​Data Sharing provides some basic tools to get and store state information in a shared location, it is not designed to be high speed or flexible. It only supports a few simple operations. Data Shares can store data in different ways, such as a database or a file.

Data Shares are bound to a specific source of data that cannot be changed. For example, a database Data Share picks a database when initialized, and cannot change later. Data Shares are also restricted in the operations they can do, such as get, set, and add. If more complex actions are needed, they can be implemented outside the class, or consider alternatives



## Node

Python

​	The Node tools are what manage an individual node. They start and stop all processes on a node, and give high level management tools and reporting services. Most importantly, they process node manifests and generate a 

# Vertex

Vertex is the custom node management tool used by Machina. It coordinates what tasks are run by which nodes, handles communication between nodes, configuration data, and monitors the overall performance of the entire network.

### Terms

Vertex: system that distributes tasks and collects information on nodes

Node: the Machina code instance running on a device

Lease: designates that a node instance should run on a specific device

Task: a single action that is to be carried out on a single node



## Load Balancing

Vertex takes inspiration from other distributed computing tools such as Apache Mesos. Every task has resource usages tied to it, and Vertex keeps track of available resources across all nodes. Tasks are sent to nodes with resources available for that task. 



## Monitoring

Vertex also keeps track of the system as a whole, such as how long tasks are taking, CPU, GPU, RAM, and storage usage for each node, overall activity, and any errors.

The resulting data is stored in a database, and can be viewed from a dashboard to get a high level view of the system and any problems it might be having



## Configuration

Vertex also handles node configuration, when a node connects to a Vertex server, it will send back the configuration data it needs. At the moment, the current plan for Machina is to have static configuration. If the configuration files are changed, the system has to restart.

However, if there is a need to update configuration files at runtime, it would be possible for the Vertex servers to send the new configuration data to all nodes. This is a possible feature that will be added if the need arises



## Usage

### Connecting to the Network

When starting up, a node will have to connect to the network. It does this by communicating with a Vertex server on startup. It tells the vertex server the node’s system information. All this information is specified manually in a file with the following format:

```ini
Vertex/Connect/Processor
Sender: Alex

{
	"Type": "Processor"
	"RAM": "10 GB"
	"CPU": "8 Cores"
	"GPU": "256 Cores"
	"Storage": "200 GB"
	"Network": "300 Mb/s"
}
```

| Property | Allowed Values       |
| -------- | -------------------- |
| Type     | Processor, Scheduler |
| RAM      | MB, GB, TB           |
| CPU      | Core, Cores          |
| GPU      | Core, Cores          |
| Storage  | MB, GB, TB           |
| Network  | Mb/s, Gb/s           |
| Name     | Any unique string    |

This data is all sent to vertex, registering the node with vertex. In return, the node is given the current configuration file. This configuration file also contains information on how to download the source code for this Machina network (typically a git repository).

The new node downloads the source code if necessary. When complete, it tells the vertex that it is ready to accept tasks.

Nodes can also be registered as schedulers. In this situation they will have a different file sent to the vertex server on startup:

```ini
Vertex/Connect/Scheduler
Sender: Brian
```

Schedulers are allowed to send, but not receive tasks. Because of this no system information is needed, and no configuration is sent back when registering. 



### Sending a Task

Tasks can be sent by schedulers, data is sent in the following format

```
LayerName/TaskName
RAM: 3 GB
CPU: 4 Core
GPU: 0 Cores
Storage: 30 MB
Network: 100 Mb/s

{
    "arg1": 15,
    "arg2": 
    {
        "arg2-1": [ 2, 3, 4 ]
    }
}
```


## Machina Tasks

Here is all the tasks that will be used to run a standard Machina network

| Name                          | Description                                       |
| ----------------------------- | ------------------------------------------------- |
| Fetch/Fetch (query)           | Gets the specified data from an external source   |
| Fetch/OverQuota (source)      | Checks if a specific source is over its quota     |
| Invoke/BuildQuerySet (ledger) | Creates a QuerySet from the name of a ledger      |
| Aggregate/Save (EntitySet)    | Saves an EntitySet to aggregators                 |
| Compute/Get (computation)     | Runs a predefined computation, returns the result |



# Layer 0 – Fetching

​	Layer 0 is the topmost layer, and directly interfaces with external APIs. Its purpose is to insulate the rest of the application from the intricacies of all the APIs. Requests made to Layer 0 are made with a protocol specifying only what data to get, and where to get it from. This request is met with a reply in a standard format containing the data requested, as well as some metadata about the request and how it was processed.

​	Layer 0 is implemented in Python, as speed is not an issue, and this code will need new modules being written frequently. It also has a small database that is used to synchronize data across multiple Layer 0 nodes

- Fetch Listener receive request
  - Send data to new thread
  - Decode data into Query Request
  - Send Request to appropriate Source
    - Limiter checks if over quota
      - If over, return with error
    - If limiter had error, return that error
    - Manager
      - Call Query
        - Build Request
        - Send Request
        - Receive Response
        - Parse Response
      - If call failed
        - Authenticate and call query again
        - If unknown issue, return an error
      - Return Query results
    - If success, notify Limiter of usage
    - Return Query results
  - Parse response to desired format
  - Reply with response



## Fetch Listener

​	The fetch listener is a small server that is listening for fetch requests on a single port. This is the core of the fetch program and will be the root that all other actions are passed through. The fetch listener doesn&#39;t do much beyond what a typical server does, and passes off all requests to the appropriate Source on a new thread



## Source

​	A Source is a place that information comes from. Sources are often connected to web APIs, but do not have to be. Sources contain information on how to interact with a specific source, such as API keys, authentication protocols, rate limits, etc.

| Attr    | Desctiption                                                  |
| ------- | ------------------------------------------------------------ |
| Name    | Used to uniquely identify the source                         |
| Limiter | Handles the Percent Quota request, which gives back the percent of the quota used as a float, 1.0 is max usage, 0.0 is no usage. Returns None if unknown. All limiters have an Over Quota request, which uses the result of Percent Quota to determine if we are over quota, if Percent Quota >= 1, returns true. < 1 returns false. None returns None (unsure). This is checked before using a query, if it is true, the query is not sent, and a message is returned saying that we are over quota |
| Data    | Holds constant data of the source, this information is retrieved from the database at initialization. It usually contains API keys, login details, etc. |
| Manager | Handles higher level communications with the source, the intended use for this module is authentication and authorization. It does high level checks on responses to check for errors and re-authenticates as required |

​	All sources should be designed so that they all behave identically across multiple Fetch nodes, any state data should be stored in the database to ensure that they all behave identically. This is mainly to reduce complexity in deciding which node to send requests to. For example, if each node had its own state for limiters, some could reach their quotas for a source, and others might not.

### Limiter

Unlimited, Rate

​	Sources can contain a limiter, which is an interchangeable module that regulates how often the source is used. This is most often used with APIs, where rate limits are common. The limiter will modify the response of the Over Quota request. All requests for queries must pass through the limiter, and if the limiter says that the source is over it&#39;s budget, that request will be canceled, and an error will be sent as a response. The limiter also must know about the total number of queries sent to the external source to know if we are currently over or under the quota. This raises a problem, because if multiple Layer 0 nodes are running, they will have trouble communicating every request that comes in. The solution to this is to have all quota information come from a table in the database. The table allows the limiters to have a central place to check and store the usage and quotas

### Data

Database, Constant, Web

​	The data is a module that is designed to provide additional information to be used within the source. The primary Data is a Database Data, which gets all information from the database at initialization. Although other Data modules could be used, such as a Constant Data, or Web Data (get from a website). A single source can have multiple data modules, all their outputs are merged together at the end.

​	Keep in mind, these are constant, and will only be set at initialization, information in the data shouldn&#39;t change often

### Manager

HTTP, HTTP Auth

​	All query requests go through a manager, it handles interactions at the protocol level. The manager is what calls the queries and ensures that they are run successfully. If they don't they, the manager will decide how to continue.



## Query

HTTP

​	A Query is the main purpose of this layer, it is the thing that retrieves data from a source and handles the response. They should be easy to work with, and easy to create, requiring very little work for most cases, but flexible enough to handle complex tasks.



## Query Flow

​	Query Flows are an abstract class that Query Request and Query Response derive from. The main use of these flows is to provide all information about a request or a response in a single object. Requests can be generated from binary with the help of encoding tools, and Responses can be converted to binary from encoding tools. This way, we can change the format we want to pass objects over sockets by changing a single parameter

### Query Request

​	A Query Request is a request sent to a Query to tell it what to do. This is created from the request received by the Fetch Listener and is passed around with all information to make the request. Some fields get added or removed as it is processed, but the Request moves through the entire chain.



| Attr      | Desctiption                                              |
| --------- | -------------------------------------------------------- |
| Start     | Time that the request was received by the Fetch Listener |
| Source    | The source this request is going to                      |
| Query     | The name of the query to run                             |
| Arguments | Any arguments that is needed to run the query            |

### Query Response

​	Like the Query Request, the Query Response contain all information needed to reply to a Query Request. It has two parts, the data, and the meta. The data is the serialized and formatted response from the source. The meta includes some extra info that is generated in processing the data. This is mostly used for debugging and system monitoring, the attributes of the meta data are below

| Meta Attr     | Description                                         |
| ------------- | --------------------------------------------------- |
| Start         | Time the request was received by the Fetch Listener |
| End           | Time the response was sent back to the requester    |
| Request Time  | Time spent handling the request                     |
| Source Time   | Time spent waiting for external source to respond   |
| Response Time | Time spend handling the response                    |
| Usage         | Current usage stored in limiter                     |
| Quota         | Max usage in limiter                                |



# Layer 1 – Invoke

​	Aggregation is what makes Machina different from most data gathering systems. It is what coordinates the entire data collection process. Specific things that the aggregation layer handles are deciding where to get data from, what kinds of data it should get, what it should get information about, and when to get that data. Each of these things will be handled by a specific type of module. Each module can be interchanged to result in high flexibility and code reuse.

​	This layer is written in C++, since there is very little custom code needed. Although custom configuration will be needed, it is mostly changing properties and configurations. Since the code isn't changing frequently, the speed optimizations of C++ become much more reasonable since these modules will rarely need maintenance or modification in production



## Trigger

​	A trigger is a module that invokes an event when something happens. That something is often a timer, but could be anything, like a button press, a field update, etc. When a timer goes off, the trigger event is invoked and all subscribed events are called on separate threads. this way the Trigger has no knowledge of what it&#39;s connected to, which is ideal, triggers should rarely be modified or customized for any specific use.



### Timer Trigger

Timer trigger is a common subtype of trigger. It will be triggered at regular intervals over time. It has a variety of settings that can be configured, which are shown below

|              |                                                              |
| ------------ | ------------------------------------------------------------ |
| Parameter    | Description                                                  |
| duration     | the timedelta between triggers in minutes                    |
| run_on_start | if true (default) this trigger will go off immediately after the timer is primed |
| quantize     | if true (default) the time will be quantized. So if trigger interval is 5 minutes and the program started at 10:02, the trigger will go off at 10:02, 10:05, 10:10. |
| offset       | Shifts quantized time. For example, if the program started at 10:02 and trigger interval is 5, with an offset of 3 minutes, it will go off at 10:02, 10:03, 10:08, 10:13. |

Note that the timer is not guaranteed to be fixed to round numbers when quantizing. Quantizing only enforces that all other triggers that are quantized will be in sync. If their durations are all 5 minutes and started around 10:00, they might go off at 10:03 and 43 seconds, but they will all go off at that time regardless of startup time or order.

## Ledger

​	Ledgers, at their core, are a 2D list of keys that will be used to retrieve data. For example, a website, might have a list of website names, id numbers, and IP addresses stored. Ledgers are updated on a schedule set by a trigger. When updated, the Ledger will access an endpoint in the Compute layer that will return the Ledger. This endpoint is where all logic of what goes into the Ledger is stored.

​	In general, each layer should only interact with the layer above and below it, Ledgers are an exception to this rule. Although generating a simple Ledger and maintaining it within the Aggregator is simple, this fails when trying to gain new leads from other sources. If you wanted to track a game, and you have their website, it would be a good idea to start tracking that website. But the Aggregator has no knowledge of video game data and cannot add that lead to the Ledger. We need the data to come from a point in the program where all data in the system is cleaned up, and available. Therefore, Ledgers should be populated from the Compute layer.

### Lead

​	A lead is a single entry in a ledger, it contains anything that may be needed to identify a source. The values within a lead is what is passed to queries as arguments. All leads for a single type will have the same structure, although some fields may be null. This is not an issue so long as the null values are not used. Unfortunately, this will not throw any errors until it reaches the Fetch layer, so it is important that the Fetch layer catches this error as soon as possible and gives an error that recommends checking the value It&#39;s reading from the Ledger

### Ledger Source

Ledger sources are given to a ledger, they describe how the ledger gets its information. Thee most common one is the SelfLedgerSource, which gets the ledger data from Machina in the compute layer.

Most notable alternate ledger source is the ConstantLedgerSource, which is used in unit testing often, it returns constant ledger data that is set at initialization

## Query Set

​	Query Sets store a list of queries to be run as a group. The intended use for Query Sets is to convert a list of Leads to a list of queries. These queries do not contain any arguments yet. To add them, a list of Leads (from a Ledger) are passed in, and each Lead will have its identifiers passed into each argument. This results in a long list of Queries that can now be used with a Fetch node to get the desired information.

### Query

​	A query is a value object what will be sent to the Fetch layer to get the data. It contains a template for the query, along with any arguments needed. For example, to get a website&#39;s view count, from source\_1 using the view\_count query, the request would look like:

```
{
	"source": "source_1",
	"query": "view_count",
    "args": 
    {
    	"domain": "google.com",
        "name": "google",
        "IP": "123.45.6.789"
    }
}
```

​	The arguments are generated from the Lead given, and contains all identifying keys. There will be a separate query for each query specified, and the source is set at the Query Set level, so it is constant for all Queries generated



## Fetch Link

​	The fetch link handles connections to the fetch nodes, it decides which node to send tasks to, and parses the data it sends and receives. There should be a single fetch link on an Aggregation Node.

​	The Fetch Link has a fetch queue, which is where any requests to the Fetch node will be put. This queue needs a large maximum size, since it will receive most fetches in a single burst. Each item is handled asynchronously with a fixed size thread pool.



## Handler

The Handler is a module that routes results from the Fetch Link to Aggregator nodes. It is responsible for reading the returned data, standardizing it, splitting it up if multiple objects are returned, and sending the resulting objects to the corresponding Aggregator.

It takes data in the following format:

```json
{
    "Type1": [{ ... }, { ... }]
    "Type2": [{ ... }]
}
```

Data is returned as lists, each list contains exactly one type of data. The Handler will split each list based on the name of its key, and send the list of data to the corresponding aggregator node.

### Clustering

​	Right now, the plan is to only have a single Aggregator for each type, however this may not be practical for large volumes of data on a single type. If this becomes a problem, Aggregators may need to be clustered by a specific field. For example, for stock prices, there could be two stock Aggregators, one deals with all stocks starting with symbols A-M, the other N-Z. In this case, the stock is clustered by its symbol. I believe this is how Cassandra DB handles the same issue, it would be worthwhile to see exactly how they deal with this issue.

​	Since this feature can cause some additional complexity in the design, and may be completely unnecessary, it&#39;s not going to be a feature by default, and should only be added if a single Aggregator is not enough to handle the volume of data.

# Layer 2 – Aggregation

​	The Aggregation layer is what decides how data is combined and computed before entering the database for storage and computation.

​	Similar to Layer 1, the only customization in this layer is changes in configuration and not in the code. So this layer is written in C++ for optimization.



## Aggregator

​	Aggregators are bound to a specific type. They determine how data should be combined and cleaned up before entering the database. They can maintain a list of &quot;partials&quot;, which are incomplete data entries. These partials are then returned to an external source when completed.

​	Aggregators can function is a wide variety of ways, the simplest pass any data they get through unchanged. Others may remember past values and &quot;forward fill&quot; them into nulls. Others may be on a timer and average all data over the span of an hour into one result, and then send that result out.

​	This is where that whole section on series from earlier comes into play. Aggregators can keep track of values over time and make estimates on data when if not available.

# Layer 3 – Data

​	The Data layer is responsible for storing information long term. Typically this will be in scylla, a simple ORM is provided to store and retrieve data from Scylla.

# Layer 4 – Compute (not implemented)

​	The Compute layer is the most heavily optimized portion of Machina. It needs to be capable of computing large volumes of information in the span of seconds. It gets this data from the Data layer, and provides GPU processing tools to produce results quickly.

# Layer 5 – Interface (not implemented)

​	The Interface layer is the publicly facing portion of Machina, it uses a standard REST API